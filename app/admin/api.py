from fastapi import APIRouter

from app.admin.users.api import router as users_router

api_router = APIRouter()

include_api = api_router.include_router

routes = (
    (users_router, "users", "users"),
)

for route in routes:
    router, prefix, tag = route

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[f"admin/{tag}"])
    else:
        include_api(router, prefix=f"/{prefix}")
