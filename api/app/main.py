from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2
from fastapi.openapi.models import OAuthFlows, OAuthFlowPassword
from jose import JWTError, jwt


from .db import init_db
from .routes import strain_routes, feeling_routes, flavor_routes, helps_with_routes, type_routes, terpene_routes
from .auth_dependencies import (
    authenticate_user,
    SECRET_KEY,
    oauth2_scheme,
    ALGORITHM,
    ADMIN_USERNAME,
)

api_version = "0.13.0"

app = FastAPI(
    title="Cannabis API",
    version=api_version,
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


# Login endpoint
@app.post("/login", tags=["Auth"])
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


# Routes
app.include_router(strain_routes.router, tags=["Strains"])
app.include_router(feeling_routes.router, tags=["Feelings"])
app.include_router(flavor_routes.router, tags=["Flavors"])
app.include_router(helps_with_routes.router, tags=["HelpsWith"])
app.include_router(type_routes.router, tags=["Types"])
app.include_router(terpene_routes.router, tags=["Terpenes"])
