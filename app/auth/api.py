from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import Token
from app.core.security import create_access_token, verify_password
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def get_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        users: UsersCRUD = Depends(get_users_crud)
) -> Token:

    user = await users.get_by_email(email=form_data.username)

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password!"
        )

    return Token(
        access_token=create_access_token(subject=str(user.uuid)),
        token_type="Bearer"
    )
