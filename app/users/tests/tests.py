from typing import Callable

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.conftest import assert_response
from app.users.models import User


@pytest.mark.asyncio
async def test_create_user(
        async_client_v1: AsyncClient,
        async_session: AsyncSession,
        test_data: dict
):
    payload = test_data["cases"]["user_create"]["payload"]
    response = await async_client_v1.post("/users", json=payload)

    assert response.status_code == 201

    got = response.json()
    want = test_data["cases"]["user_create"]["want"]

    assert_response(got, want)

    statement = select(User)
    results = await async_session.execute(statement=statement)
    user = results.scalar_one()  # type: User

    assert user


@pytest.mark.asyncio
async def test_get_me(
        async_client_v1: AsyncClient,
        async_session: AsyncSession,
        create_user: Callable,
        test_data: dict
):
    headers = await create_user(
        async_session,
        test_data["cases"]["user_get"]["init"]["user"]
    )

    response = await async_client_v1.get("/users/me", headers=headers)

    assert response.status_code == 200

    got = response.json()
    want = test_data["cases"]["user_get"]["want"]

    assert_response(got, want)


@pytest.mark.asyncio
async def test_patch_me(
        async_client_v1: AsyncClient,
        async_session: AsyncSession,
        create_user: Callable,
        test_data: dict
):
    headers = await create_user(
        async_session,
        test_data["cases"]["user_patch"]["init"]["user"]
    )

    payload = test_data["cases"]["user_patch"]["payload"]

    response = await async_client_v1.patch(
        "/users/me",
        json=payload,
        headers=headers
    )

    assert response.status_code == 200

    got = response.json()
    want = test_data["cases"]["user_patch"]["want"]

    assert_response(got, want)


@pytest.mark.asyncio
async def test_delete_me(
        async_client_v1: AsyncClient,
        async_session: AsyncSession,
        create_user: Callable,
        test_data: dict
):
    headers = await create_user(
        async_session,
        test_data["cases"]["user_delete"]["init"]["user"]
    )

    response = await async_client_v1.delete("/users/me", headers=headers)

    assert response.status_code == 200

    got = response.json()
    want = test_data["cases"]["user_delete"]["want"]

    assert_response(got, want)

    statement = select(User).where(
        User.uuid == test_data["cases"]["user_delete"]["init"]["user"]["uuid"]
    )
    results = await async_session.execute(statement=statement)
    user = results.scalar_one()  # type: User

    assert user.is_deleted
