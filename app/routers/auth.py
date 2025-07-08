from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import Annotated
from ..database.database import postgresDB
import logging
from os import getenv
from dotenv import load_dotenv

load_dotenv()

auth_logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
crypt = CryptContext(schemes="argon2") #do it once for performance

secret = getenv("secret")
if not secret:
    raise ValueError("Secret value is missing")

algorithm = "HS256" 

class Token(BaseModel):
    sub: str #unique identifier of the user
    iss: str #issuer
    #iat: datetime #time of issuing
   # exp: datetime #time of expiration

class User(BaseModel):
    username: str
    password: str


def gen_hash( password: str ):
    hash = crypt.hash(password)
    auth_logger.info("Generating password hash")
    return hash

def check_hash(hash: str, password: str)->str:
    if crypt.verify(password, hash):
        return True
    return False

def gen_jwt(id: int)-> str:
    iss_at = datetime.now(timezone.utc)
    exp = datetime.now(timezone.utc) +  timedelta(hours=1)
    data = {
            "sub": id,
            "iss": "k-homelab",
            "iat": iss_at, #using jwt registered claims for issue at and expiration 
            "exp": exp #only then you can pass datetime object to encode
    }
    token = jwt.encode( data, secret, algorithm)
    auth_logger.info("Generating JWT token")
    return token

def read_jwt(jwt_token: str)-> dict:
    decoded_token = jwt.decode(jwt_token,secret,algorithms=[algorithm])
    payload = {
        **decoded_token
    }
    payload["iat"] = datetime.fromtimestamp(decoded_token['iat'], tz=timezone.utc)
    payload["exp"] = datetime.fromtimestamp(decoded_token['exp'], tz=timezone.utc)
    return payload

@auth_router.post("/user_add")
async def user_add(user: User):
    async with postgresDB() as db:
        try:
            check_user = await db.get_user(user.username)
            if not check_user:
                password_hash = gen_hash(user.password)
                await db.auth_insert({"username" : user.username,"password_hash" : password_hash})
                return {"msg": "User created", "username" : user.username}
            else:
                return {"msg" : "Username already taken"}
        except Exception as error:
            raise HTTPException(status_code=500,detail=f'Failed to add user into table USERS: {error}')


@auth_router.post("/token")
async def auth(formdata : Annotated[OAuth2PasswordRequestForm, Depends()]):
    async with postgresDB() as db:
        user_data = await db.get_user(formdata.username)
        if user_data:
            if check_hash(user_data["password_hash"],formdata.password):
                token = gen_jwt( user_data["id"] )
                return {"token" : token}
        auth_logger.warning(f"Failed login attempt for username: {formdata.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )