from datetime import date
from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from app.bookings.schemas import SBookingView, SBooking
from app.bookings.service import BookingService
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.models import Users
from app.users.dependencies import get_current_user
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.get("")
async def get_bookings(
        user: Users = Depends(get_current_user)
        ) -> list[SBookingView]:
    return await BookingService.get_bookings_view(user.id)


@router.post("")
async def add_booking(
    room_id: int, date_from: date, date_to: date,
    user: Users = Depends(get_current_user),
    
):
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = SBooking.model_validate(booking, from_attributes=True).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)


@router.delete("/{booking_id}", status_code=204)
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user)
):
    await BookingService.delete(id=booking_id, user_id=user.id)
