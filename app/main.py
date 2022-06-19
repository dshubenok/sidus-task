import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import settings
from app.caching.core import Cache
from app.core.models import HealthCheck
from app.router.api_v1.endpoints import api_router

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["content-disposition", "content-type"]
)


@app.on_event("startup")
async def startup():
    Cache.init(
        url=settings.cache_redis,
        encoding="utf8",
        decode_responses=True,
        prefix=settings.cache_prefix
    )


@app.get("/", response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description
    }


app.include_router(api_router, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
