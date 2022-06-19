from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode

from app import settings
from app.auth.models import TokenPayload
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud
from app.users.models import UserAuth

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/auth/access-token"
)


async def get_current_user(
        users: UsersCRUD = Depends(get_users_crud),
        token: str = Depends(reusable_oauth2)
) -> UserAuth:
    try:
        payload = decode(
            jwt=token,
            key=settings.auth_secret_key,
            algorithms=[settings.auth_algorithm]
        )
        token_data = TokenPayload(**payload)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user hasn't been authorized!"
        )

    user = await users.get(user_id=token_data.sub)
    return user


def get_current_active_user(
        user: UserAuth = Depends(get_current_user)
) -> UserAuth:
    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user is not active!"
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user is not verified!"
        )

    return user


def get_current_staff(
        current_user: UserAuth = Depends(get_current_user)
) -> UserAuth:
    staff_privileges = current_user.is_staff or current_user.is_superuser

    if not staff_privileges or current_user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges!"
        )
    return current_user


def get_current_superuser(
        current_user: UserAuth = Depends(get_current_user)
) -> UserAuth:
    if not current_user.is_superuser or current_user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges!"
        )
    return current_user
