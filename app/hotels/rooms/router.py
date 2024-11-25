from datetime import date

from fastapi_cache.decorator import cache

from app.exceptions import DateFromMustBeAfterCurrentDate
from app.hotels.rooms.schemas import SRoomInfo
from app.hotels.rooms.service import RoomService
from app.hotels.router import router


@router.get("/{hotel_id}/rooms")
@cache(expire=30)
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> list[SRoomInfo]:
    if date_from > date_to:
        raise DateFromMustBeAfterCurrentDate
    return await RoomService.get_rooms_left_in_hotel(hotel_id, date_from, date_to)
