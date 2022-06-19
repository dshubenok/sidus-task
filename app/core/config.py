from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    # Database
    db_async_connection_str: str
    db_async_test_connection_str: str
    db_exclude_tables: List[str]

    # Cache
    cache_redis: str
    cache_prefix: str

    # Celery
    celery_backend_db: str
    celery_broker: str

    # Security
    auth_algorithm: str
    auth_token_expire: int

    auth_secret_key: str
    email_secret_key: str

    cors_origins: List[str]

    # Email
    email_account: str
    email_password: str
    email_server: str
    email_port: int
