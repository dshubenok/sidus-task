from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import func, or_, select, update
from sqlalchemy.sql.operators import ilike_op
from sqlmodel.ext.asyncio.session import AsyncSession

from app.caching.core import cache, cache_update, cache_remove
from app.core.decorators import handle_integrity_error
from app.core.security import get_password_hash
from app.users.models import (User, UserCreate, UserList, UserPatch, UserRead,
                              UserStaffPatch, UserStaffRead)


class UsersCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    @handle_integrity_error(detail="The user already exists!")
    async def create(self, data: UserCreate) -> User:
        values = data.dict()
        values["hashed_password"] = get_password_hash(
            password=values["password_1"]
        )

        user = User(**values)
        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    @cache(namespace="users", model=User, keys=["user_id"])
    async def get(
            self,
            user_id: str | UUID,
            no_cache: bool = False,  # noqa: indirect usage
            by_staff: bool = False
    ) -> User:
        where_clause = [User.uuid == user_id]
        if not by_staff:
            where_clause.append(User.is_deleted == False)
        statement = select(
            User
        ).where(
           *where_clause
        )
        results = await self.session.execute(statement=statement)
        user = results.scalar_one_or_none()  # type: User | None

        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"The User(uuid={user_id}) hasn't been found!"
            )

        return user

    async def list(
            self,
            substring: str = None,
            offset: int = 0,
            limit: int = 10,
            by_staff: bool = False
    ) -> UserList:
        model = UserStaffRead if by_staff else UserRead

        where_clause = []
        if not by_staff:
            where_clause.append(User.is_deleted == False)

        if substring:
            where_clause.append(
                or_(
                    ilike_op(User.email, f"%{substring}%"),
                    ilike_op(User.first_name, f"%{substring}%"),
                    ilike_op(User.last_name, f"%{substring}%")
                )
            )

        statement = select(
            User
        ).where(
            *where_clause
        ).order_by(
            User.first_name
        ).offset(offset).limit(limit)
        results = await self.session.execute(statement=statement)
        items = [model.parse_obj(r) for r in results.scalars().all()]

        statement = select(
            func.count(User.uuid).label("count")
        ).where(
            *where_clause
        )
        results = await self.session.execute(statement=statement)
        count = results.first()["count"]

        return UserList(items=items, count=count)

    @cache_update(namespace="users", keys=["user_id"])
    async def patch(
            self,
            user_id: str | UUID,
            data: UserPatch | UserStaffPatch
    ) -> User:
        values = data.dict(exclude_unset=True)

        user = await self.get(user_id=user_id, no_cache=True)
        for k, v in values.items():
            setattr(user, k, v)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    @cache_remove(namespace="users", keys=["user_id"])
    async def delete(self, user_id: str | UUID) -> bool:
        statement = update(
            User
        ).where(
            User.uuid == user_id
        ).values(
            {"is_deleted": True}
        )
        await self.session.execute(statement=statement)
        await self.session.commit()

        return True

    async def get_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        results = await self.session.execute(statement=statement)
        user = results.scalar_one_or_none()
        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f"The User(email={email}) hasn't been found!"
            )

        return user
