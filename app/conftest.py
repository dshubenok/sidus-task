import asyncio
import json
import os
from typing import Callable, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app import settings
from app.core.db import async_engine
from app.core.security import create_access_token as get_token
from app.main import app
from app.users.models import User


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client_v1():
    async with AsyncClient(
            app=app,
            base_url=f"http://{settings.api_v1_prefix}"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await async_engine.dispose()


@pytest.fixture(scope="function")
def test_data() -> dict:
    path = os.getenv('PYTEST_CURRENT_TEST')
    path = os.path.join(*os.path.split(path)[:-1], "data", "data.json")

    if not os.path.exists(path):
        path = os.path.join("data", "data.json")

    with open(path, "r") as file:
        data = json.loads(file.read())

    return data


@pytest_asyncio.fixture
async def create_user() -> Callable:
    async def new_user(
            session: AsyncSession,
            user_data: dict
    ) -> dict:
        statement = insert(User).values(user_data)
        await session.execute(statement=statement)

        await session.commit()

        headers = {
            "Authorization": f"Bearer {get_token(user_data['uuid'])}"
        }

        return headers

    return new_user


def assert_response(got: dict, want: dict):
    for k, v in want.items():
        got_attr = got.get(k)
        if isinstance(got_attr, dict):
            assert_response(got_attr, v)
        else:
            assert got_attr == v
