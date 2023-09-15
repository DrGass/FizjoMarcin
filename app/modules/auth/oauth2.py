from fastapi import Depends, HTTPException, status
import modules.auth.token as token
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(data: str = Depends(oauth2_scheme)):
    return token.verify_token(data)
