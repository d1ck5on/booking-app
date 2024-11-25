from datetime import date

from pydantic import BaseModel

from app.hotels.rooms.schemas import SRoomCropped


class SBookingCropped(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class SBooking(SBookingCropped):
    id: int


class SBookingView(SBookingCropped, SRoomCropped):
    pass
