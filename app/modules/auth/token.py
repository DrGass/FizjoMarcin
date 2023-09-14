from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, status
import modules.schemas.token_schema as token_schema

from env import get_env
env = get_env()

SECRET_KEY = "28b802dd320593ee6e84523870ffe73b046aefce92450dfbfef77dadf2f5a8c4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    if env.environment != "development":
        return {"email": "test@test.com"}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception
