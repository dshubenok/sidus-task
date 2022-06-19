from datetime import datetime, timedelta
from uuid import UUID

from jwt import encode as jwt_encode
from passlib.context import CryptContext
from pydantic import EmailStr

from app import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        subject: str,
        expires_delta: timedelta = None
) -> str:

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.auth_token_expire
        )

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt_encode(
        payload=to_encode,
        key=settings.auth_secret_key,
        algorithm=settings.auth_algorithm
    )

    return encoded_jwt


def create_email_verify_token(
        subject: str | UUID,
        email: EmailStr,
        expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.auth_token_expire
        )

    to_encode = {"exp": expire, "sub": str(subject), "attr": str(email)}
    encoded_jwt = jwt_encode(
        payload=to_encode,
        key=settings.email_secret_key,
        algorithm=settings.auth_algorithm
    )

    return encoded_jwt
