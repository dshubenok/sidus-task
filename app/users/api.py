import logging

from fastapi import APIRouter, Depends
from fastapi import status as http_status
from sys import modules

from app.auth.dependencies import get_current_user
from app.core.models import StatusMessage
from app.routines.app import celery_app
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud
from app.users.models import User, UserCreate, UserPatch, UserRead
from fastapi.background import BackgroundTasks


router = APIRouter()


log = logging.getLogger(__name__)


def background_on_message(task):
    log.info(task.get(propagate=False))


@router.post(
    "",
    response_model=UserRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_me_user(
        data: UserCreate,
        background_tasks: BackgroundTasks,
        users: UsersCRUD = Depends(get_users_crud)
):
    user = await users.create(data=data)

    if "pytest" not in modules:
        task = celery_app.send_task(
            "greetings_email",
            kwargs={
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        )
        background_tasks.add_task(background_on_message, task)

    return user


@router.get(
    "/me",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def get_me(
        users: UsersCRUD = Depends(get_users_crud),
        user: User = Depends(get_current_user)
):
    user = await users.get(user_id=user.uuid)
    return user


@router.patch(
    "/me",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def patch_me(
        data: UserPatch,
        users: UsersCRUD = Depends(get_users_crud),
        user: User = Depends(get_current_user)
):
    user = await users.patch(user_id=user.uuid, data=data)
    return user


@router.delete(
    "/me",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_me(
        users: UsersCRUD = Depends(get_users_crud),
        user: User = Depends(get_current_user)
):
    deleted = await users.delete(user_id=user.uuid)
    return {"status": deleted, "message": "The user has been deleted!"}
