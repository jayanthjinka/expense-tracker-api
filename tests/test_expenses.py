import pytest
import httpx
from httpx import ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_get_expenses_requires_auth():

    transport = ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/expenses/")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_expense_authenticated():

    transport = ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:

        # signup
        await ac.post(
            "/auth/signup",
            json={"email": "testuser@example.com", "password": "password123"},
        )

        # login
        login_response = await ac.post(
            "/auth/login",
            data={"username": "testuser@example.com", "password": "password123"},
        )

        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # create expense
        response = await ac.post(
            "/expenses/",
            json={
                "amount": 100,
                "category": "Food",
                "description": "Lunch",
                "date": "2026-01-01",
            },
            headers=headers,
        )

    assert response.status_code == 200
    assert response.json()["amount"] == 100


@pytest.mark.asyncio
async def test_update_expense():

    transport = ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:

        # signup
        await ac.post(
            "/auth/signup",
            json={"email": "testupdate@example.com", "password": "password123"},
        )

        # login
        login_response = await ac.post(
            "/auth/login",
            data={"username": "testupdate@example.com", "password": "password123"},
        )

        token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # create expense
        create_response = await ac.post(
            "/expenses/",
            json={
                "amount": 100,
                "category": "Food",
                "description": "Lunch",
                "date": "2026-01-01",
            },
            headers=headers,
        )

        expense = create_response.json()

        # update expense
        update_response = await ac.patch(
            f"/expenses/{expense['id']}",
            json={"amount": 150, "description": "Updated Lunch"},
            headers=headers,
        )

    assert update_response.status_code == 200
    assert update_response.json()["amount"] == 150
