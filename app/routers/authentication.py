from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(tags=["Authentication"])

from app.modules.database import SessionLocal, get_db
from app.modules.auth.hashing import Hash
from app.modules.auth.token import create_access_token
import app.modules.schemas.authentication_schema as auth_schema
import app.modules.models.user_model as user_model 


@router.post("/login",)
def login(request: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid Credentials",
        )
    if not Hash.verify(request.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incorrect Password",
        )

    access_token = create_access_token(data={"sub": user.email}) 
    return {"access token": access_token, "token_type": "bearer"}
