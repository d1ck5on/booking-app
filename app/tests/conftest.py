from datetime import datetime
import json
import pytest
from sqlalchemy import insert
from app.main import app as fastapi_app
from app.config import settings
from app.database import Base, sessionmaker, engine

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users

from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    bookings = open_mock_json("bookings")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with sessionmaker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def logged_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "test@test.com",
            "password": "test",
        })
        assert ac.cookies["booking_access_token"]
        yield ac
