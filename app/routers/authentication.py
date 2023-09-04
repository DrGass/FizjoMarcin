from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])

from app.modules.database import get_db

# from app.modules.auth.token import create_access_token
import app.modules.models.user_model as user_model
import app.modules.schemas.token_schema as token_schema
import app.modules.schemas.user_schema as user_schema

# from app.modules.auth.oauth2 import get_current_user

# @router.post(
#     "/token",response_model=token_schema.Token
# )
# def login(
#     request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
# ):
#     user = (
#         db.query(user_model.User)
#         .filter(user_model.User.username == request.username)
#         .first()
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Invalid Credentials",
#         )
#     if not Hash.verify(request.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Incorrect Password",
#         )
#     print(user.username)
#     access_token = create_access_token(data={"sub": user.username})
#     print(f"access_token {access_token}")
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/get_me", response_model=user_schema.User)
# def read_users_me(
#     current_user: Annotated[user_schema.User, Depends(get_current_user)]
# ):
#     return current_user

SECRET_KEY = "28b802dd320593ee6e84523870ffe73b046aefce92450dfbfef77dadf2f5a8c4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    to_encode = data.copy()
    print("to encode", to_encode)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    print("to encode after update", to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("already encoded: ", encoded_jwt)
    return encoded_jwt


# def verify_token(token: str, credentials_exception):
#     try:
#         print("przed ",token)
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print("po")
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = token_schema.TokenData(username=username)
#         print(token_data)
#         return token_data
#     except JWTError:
#         raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("przed token", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("po token ", token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
        print("token_data", token_data)
        return token_data

    except JWTError:
        raise credentials_exception


@router.post("/token", response_model=token_schema.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(user_model.User)
        .filter(user_model.User.username == form_data.username)
        .first()
    )
    print(user)
    access_token = create_access_token(data={"sub": user.username})
    print("access_token w poscie:", access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=user_schema.User)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]
