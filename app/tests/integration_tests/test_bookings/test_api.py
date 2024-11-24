from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    *[(4, "2030-05-01", "2030-05-05", i, 200) for i in range(3, 11)],
    (4, "2030-05-01", "2030-05-05", 10, 409),
    (4, "2030-05-01", "2030-05-05", 10, 409),
])
@pytest.mark.asyncio
async def test_add_and_get_booking(room_id, date_from, date_to, booked_rooms, status_code, logged_client: AsyncClient):
    response = await logged_client.post("/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    
    assert response.status_code == status_code

    response = await logged_client.get("/bookings")
    assert len(response.json()) == booked_rooms
