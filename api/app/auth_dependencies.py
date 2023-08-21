from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2
from fastapi.openapi.models import OAuthFlows, OAuthFlowPassword
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
import os
from datetime import datetime, timedelta



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