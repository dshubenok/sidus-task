from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr, root_validator, validator
from sqlalchemy import Column, text
from sqlmodel import Field, SQLModel

from app.core.models import TimestampModel, UUIDModel
from app.core.validators import enum_validator
from app.users.types import usr_gender_type

prefix = "usr"


class UserBase(SQLModel):
    first_name: str = Field(max_length=127, nullable=False, index=True)
    last_name: str = Field(max_length=127, nullable=False, index=True)

    gender: Optional[str] = Field(
        sa_column=Column("gender", usr_gender_type),
        nullable=True,
    )

    date_of_birth: Optional[date] = Field(nullable=True)


class UserAuth(SQLModel):
    email_verified: bool = Field(
        nullable=False,
        default=False,
        sa_column_kwargs={"server_default": text("false")}
    )

    is_superuser: bool = Field(
        nullable=False,
        default=False,
        sa_column_kwargs={"server_default": text("false")}
    )

    is_staff: bool = Field(
        nullable=False,
        default=False,
        sa_column_kwargs={"server_default": text("false")}
    )

    is_deleted: bool = Field(
        nullable=False,
        default=False,
        sa_column_kwargs={"server_default": text("false")}
    )


class User(
    TimestampModel,
    UserAuth,
    UserBase,
    UUIDModel,
    table=True
):
    __tablename__ = f"{prefix}_users"

    email: EmailStr = Field(
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True}
    )
    hashed_password: str


class UserCreate(UserBase):
    email: EmailStr

    password_1: str = Field(min_length=8, max_length=24)
    password_2: str = Field(min_length=8, max_length=24)

    @validator("gender")
    def check_gender(cls, value):  # noqa: class method
        return enum_validator(
            field="gender",
            value=value,
            enum=usr_gender_type,
            required=False
        )

    @root_validator()
    def passwords(cls, values: dict):  # noqa: classmethod
        if values.get("password_1") != values.get("password_2"):
            raise ValueError("Passwords don't match!")

        symbols = r'~`! @#$%^&*()_-+={[}]|\:;"\'<,>.?/'

        if not any([s in values["password_1"] for s in symbols]):
            raise ValueError(
                f"The password must contain "
                f"at least one of the symbols: {symbols}!"
            )

        if not any([s.isdigit() for s in values["password_1"]]):
            raise ValueError(
                "The password must contain at least one digit!"
            )

        if not any([s.islower() for s in values["password_1"]]):
            raise ValueError(
                "The password must contain at least one lowercase letter!"
            )

        if not any([s.isupper() for s in values["password_1"]]):
            raise ValueError(
                "The password must contain at least one uppercase letter!"
            )

        if not any([values.get("email"), values.get("phone")]):
            raise ValueError(
                "At least one of email or phone number must be provided!"
            )

        return values


class UserRead(UserBase, UUIDModel):
    email: EmailStr


class UserStaffRead(UserAuth, UserBase, UUIDModel):
    ...


class UserPatch(UserBase):
    first_name: Optional[str] = Field(max_length=127)
    last_name: Optional[str] = Field(max_length=127)

    @validator("gender")
    def check_gender(cls, value):  # noqa: class method
        return enum_validator(
            field="gender",
            value=value,
            enum=usr_gender_type,
            required=False
        )


class UserStaffPatch(UserAuth, UserPatch):
    ...


class UserList(BaseModel):
    items: List[UserStaffRead | UserRead]
    count: int
