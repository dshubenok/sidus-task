
from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.auth.dependencies import get_current_staff
from app.core.models import StatusMessage
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud
from app.users.models import User, UserList, UserStaffPatch, UserStaffRead


router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=UserStaffRead,
    status_code=http_status.HTTP_200_OK
)
async def get_user_by_id(
        user_id: str,
        users: UsersCRUD = Depends(get_users_crud),
        staff: User = Depends(get_current_staff)  # noqa: indirect usage
):
    user = await users.get(user_id=user_id, by_staff=True, no_cache=True)
    return user


@router.get(
    "",
    response_model=UserList,
    status_code=http_status.HTTP_200_OK
)
async def list_users(
        substring: str = None,
        offset: int = 0,
        limit: int = 10,
        users: UsersCRUD = Depends(get_users_crud),
        staff: User = Depends(get_current_staff)  # noqa: indirect usage
):
    user = await users.list(
        substring=substring,
        limit=limit,
        offset=offset,
        by_staff=True
    )

    return user


@router.patch(
    "/{user_id}",
    response_model=UserStaffRead,
    status_code=http_status.HTTP_200_OK
)
async def patch_user(
        user_id: str,
        data: UserStaffPatch,
        users: UsersCRUD = Depends(get_users_crud),
        staff: User = Depends(get_current_staff)  # noqa: indirect usage
):
    user = await users.patch(user_id=user_id, data=data)
    return user


@router.delete(
    "/{user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_me(
        user_id: str,
        users: UsersCRUD = Depends(get_users_crud),
        staff: User = Depends(get_current_staff)  # noqa: indirect usage
):
    deleted = await users.delete(user_id=user_id)
    return {"status": deleted, "message": "The user has been deleted!"}
