from fastapi import APIRouter

from app.admin.api import api_router as admin
from app.auth.api import router as auth
from app.users.api import router as users

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (admin, "admin", ""),
    (auth, "auth", "auth"),
    (users, "users", "users"),
)

for router in routers:
    router, prefix, tag = router

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
