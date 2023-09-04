from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import app.modules.schemas.token_schema as token_schema

SECRET_KEY = "28b802dd320593ee6e84523870ffe73b046aefce92450dfbfef77dadf2f5a8c4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600


def create_access_token(data: dict):
    to_encode = data.copy()
    print("to encode",to_encode)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print("to encode after update",to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        print("przed ",token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("po")
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
        print(token_data)
        return token_data
    except JWTError:
        raise credentials_exception

