from datetime import date

from sqlalchemy import and_, func, or_, select

from app.bookings.models import Bookings
from app.database import sessionmaker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService


class HotelService(BaseService):
    model = Hotels

    @classmethod
    async def get_hotels_with_rooms(cls, location: str, date_from: date, date_to: date):
        async with sessionmaker() as session:
            booked_rooms_count = (
                select(Bookings.room_id, func.count(Bookings.room_id).label("count"))
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_to >= date_from, Bookings.date_to <= date_to
                        ),
                    )
                )
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )

            get_hotels = (
                select(
                    Hotels.__table__.columns,
                    func.sum(
                        Rooms.quantity - func.coalesce(booked_rooms_count.c.count, 0)
                    ).label("rooms_left"),
                )
                .select_from(Hotels)
                .join(Rooms, Rooms.hotel_id == Hotels.id)
                .join(
                    booked_rooms_count,
                    booked_rooms_count.c.room_id == Rooms.id,
                    isouter=True,
                )
                .where(Hotels.location.ilike(f"%{location}%"))
                .group_by(Hotels.id)
                .having(
                    func.sum(
                        Rooms.quantity - func.coalesce(booked_rooms_count.c.count, 0)
                    )
                    > 0
                )
            )

            hotels = await session.execute(get_hotels)
            return hotels.mappings().all()
