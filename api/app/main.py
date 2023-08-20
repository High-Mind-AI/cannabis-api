from fastapi import FastAPI, HTTPException, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2
from fastapi.openapi.models import OAuthFlows, OAuthFlowPassword
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime, timedelta
import requests
import os


from .db import get_session, init_db
from .models import Strain, Feeling, StrainFeeling
from .schemas.strain import StrainCreate, StrainUpdate, StrainInDB
from .schemas.feeling import FeelingCreate, FeelingUpdate, FeelingInDB


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hash context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Define OAuth2 flow for Swagger UI
oauth_flow = {"tokenUrl": "login"}
oauth_flows = OAuthFlows(password=OAuthFlowPassword(tokenUrl="/login"))


ADMIN_USERNAME = os.getenv("ADMIN_API_USERNAME")
ADMIN_PASSWORD_HASH = pwd_context.hash(os.getenv("ADMIN_API_PASSWORD"))


app = FastAPI(
    title="Cannabis API",
    version="0.0.1",
    description="An API of cannabis strains and descriptions.",
    openapi_tags=[],
    components={
        "securitySchemes": {
            "oauth2_scheme": OAuth2(
                flows=OAuthFlows(password=OAuthFlowPassword(tokenUrl="login"))
            )
        }
    },
    security=[{"oauth2_scheme": []}],
)

origins = [
    "http://localhost:8004",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await init_db()


# Verify user credentials
def verify_user(username: str, password: str):
    if username == ADMIN_USERNAME and pwd_context.verify(password, ADMIN_PASSWORD_HASH):
        return True
    else:
        return False


# Define a function to check if the current user is an admin
def get_admin_user(current_user: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token to get the payload
        payload = jwt.decode(current_user, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the 'sub' claim (username) from the payload
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if the user is an admin
    if username != ADMIN_USERNAME:
        raise HTTPException(status_code=403, detail="Not authorized")

    return username


# Authenticate user and generate access token
def authenticate_user(username: str, password: str):
    if verify_user(username, password):
        access_token_expires = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token_payload = {"sub": username, "exp": access_token_expires}
        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


# Login endpoint
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return authenticate_user(form_data.username, form_data.password)


# Protected endpoint
@app.get("/admin-only")
async def admin_only(current_user: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token to get the payload
        payload = jwt.decode(current_user, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the 'sub' claim (username) from the payload
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")
    if username != ADMIN_USERNAME:
        raise HTTPException(status_code=403, detail="Not authorized")
    else:
        return {"message": "Hello, admin!"}


@app.get("/strains/{strain_name}")
async def get_strain(strain_name: str, session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(Strain).where(func.lower(Strain.name) == strain_name.lower())
        result = await s.execute(stmt)
        strain = result.scalar()
        if strain is None:
            raise HTTPException(
                status_code=404, detail=f"Strain {strain_name} not found"
            )
        return strain


@app.get("/strains")
async def get_strains(count: int = 20, session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(Strain).order_by(Strain.id).limit(count)
        result = await s.execute(stmt)
        strains = result.scalars().all()
        return strains


@app.post("/strains", response_model=List[StrainInDB])
async def create_strains(
    strains: List[StrainCreate],
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    created_strains = []

    async with session as s:
        # Begin a transaction
        await s.begin()

        for strain in strains:
            # Verify that all feelings exist
            feeling_objs = []
            for feeling_id in strain.feelings:
                stmt = select(Feeling).filter_by(id=feeling_id)
                result = await s.execute(stmt)
                feeling_obj = result.scalars().first()
                if not feeling_obj:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Feeling with ID {feeling_id} does not exist",
                    )
                feeling_objs.append(feeling_obj)

            # Create the new strain without feelings
            new_strain = Strain(**strain.dict(exclude={"feelings"}))

            # Set the feelings
            new_strain.feelings = feeling_objs

            s.add(new_strain)
            await s.flush()  # Ensure new_strain gets an ID
            created_strains.append(new_strain)

        try:
            await s.commit()
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Strain already exists")

    # Since the strains are committed, you can directly return the created_strains list
    return created_strains


# Update an existing Strain
@app.put("/strains/{strain_id}", response_model=StrainInDB)
async def update_strain(
    strain_id: int,
    strain: StrainUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_strain = await s.get(Strain, strain_id)
        if existing_strain is None:
            raise HTTPException(status_code=404, detail="Strain not found")
        for key, value in strain.dict(exclude_unset=True).items():
            setattr(existing_strain, key, value)
        try:
            await s.commit()
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Strain already exists...")
        return existing_strain


# Delete an existing Strain
@app.delete("/strains/{strain_id}", response_model=dict)
async def delete_strain(
    strain_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_strain = await s.get(Strain, strain_id)
        if existing_strain is None:
            raise HTTPException(status_code=404, detail="Strain not found")
        await s.delete(existing_strain)
        await s.commit()
        return {"Strain deleted": existing_strain.name}


# Get All Feelings
@app.get("/feelings", response_model=List[FeelingInDB])
async def get_all_feelings(session: AsyncSession = Depends(get_session)):
    async with session as s:
        stmt = select(Feeling).order_by(Feeling.id)
        result = await s.execute(stmt)
        feelings = result.scalars().all()
        return [FeelingInDB(**f.__dict__) for f in feelings]


# Feelings Create
@app.post("/feelings", response_model=FeelingInDB)
async def create_feeling(
    feeling: FeelingCreate,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        new_feeling = Feeling(**feeling.dict())
        s.add(new_feeling)
        try:
            await s.commit()
            await s.refresh(new_feeling)
        except IntegrityError:
            await s.rollback()
            raise HTTPException(status_code=400, detail="Feeling already exists")
    return FeelingInDB(**new_feeling.__dict__)  # Convert ORM model to Pydantic


# Feelings Delete
@app.delete("/feelings/{feeling_id}", response_model=dict)
async def delete_feeling(
    feeling_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_admin_user),
):
    async with session as s:
        existing_feeling = await s.get(Feeling, feeling_id)
        if existing_feeling is None:
            raise HTTPException(status_code=404, detail="Feeling not found")
        await s.delete(existing_feeling)
        await s.commit()
        return {"Feeling deleted": existing_feeling.name}
