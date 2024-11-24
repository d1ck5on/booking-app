from datetime import date
from sqlalchemy import func, select, or_, and_
from app.bookings.models import Bookings
from app.service.base import BaseService
from app.hotels.rooms.models import Rooms
from app.database import sessionmaker


class RoomService(BaseService):
    model = Rooms

    @classmethod
    async def get_rooms_left_in_hotel(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date):
        booked_rooms_count = select(
                Bookings.room_id,
                func.count(Bookings.room_id).label("count")
                ).where(
                or_(
                    and_(Bookings.date_from >= date_from,
                         Bookings.date_from <= date_to),
                    and_(Bookings.date_to >= date_from,
                         Bookings.date_to <= date_to)
                )
                ).group_by(Bookings.room_id).cte("booked_rooms")

        get_rooms = select(
            Rooms.__table__.columns,
            ((date_to - date_from).days * Rooms.price).label("total_cost"),
            (Rooms.quantity - func.coalesce(booked_rooms_count.c.count, 0)).label("rooms_left")
        ).select_from(Rooms).join(
            booked_rooms_count,
            booked_rooms_count.c.room_id == Rooms.id,
            isouter=True
        ).where(Rooms.hotel_id == hotel_id)

        async with sessionmaker() as session:
            rooms = await session.execute(get_rooms)
            return rooms.mappings().all()
