import asyncio
from datetime import date, datetime
from fastapi import APIRouter
from app.hotels.schemas import SHotelInfo, SHotel
from app.hotels.service import HotelService
from fastapi_cache.decorator import cache
from app.exceptions import (
    DateFromCannotBeAfterDateTo,
    DateFromMustBeAfterCurrentDate,
    HotelDoesNotExists
)


router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date,
        date_to: date) -> list[SHotelInfo]:
    if (date_from > date_to):
        raise DateFromCannotBeAfterDateTo
    if (date_from < datetime.now().date()):
        raise DateFromMustBeAfterCurrentDate
    hotels = await HotelService.get_hotels_with_rooms(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
@cache(expire=30)
async def get_hotel_by_id(hotel_id: int) -> SHotel:
    hotel = await HotelService.find_by_id(hotel_id)
    if not hotel:
        raise HotelDoesNotExists
    return hotel
