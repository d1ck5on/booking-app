from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.database import sessionmaker
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService
from app.logger import logger


class BookingService(BaseService):
    model = Bookings

    @classmethod
    async def get_bookings_view(cls, user_id: int):
        get_bookings = (
            select(
                Bookings.room_id,
                Bookings.user_id,
                Bookings.date_from,
                Bookings.date_to,
                Bookings.price,
                Bookings.total_cost,
                Bookings.total_days,
                Rooms.image_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
            )
            .select_from(Bookings)
            .join(Rooms, Rooms.id == Bookings.room_id)
            .where(Bookings.user_id == user_id)
        )
        async with sessionmaker() as session:
            bookings = await session.execute(get_bookings)
            return bookings.mappings().all()

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        with booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
            (date_to >= '2023-05-15' AND date_to <= '2023-06-20')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
        WHERE rooms.id = 1
        GROUP BY rooms.id
        """
        try:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_to >= date_from, Bookings.date_to <= date_to
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.id)
            )

            async with sessionmaker() as session:
                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar()

            if rooms_left <= 0:
                return None

            get_price = select(Rooms.price).filter_by(id=room_id)
            async with sessionmaker() as session:
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()
        except (SQLAlchemyError, Exception) as e:
            extra = {
                "user_id" : user_id,
                "room_id" : room_id,
                "date_from" : date_from,
                "date_to" : date_to,
            }
            logger.error(
                msg=f"{type(e).__name__} Exc: Cannot add booking",
                extra=extra,
                exc_info=True,
            )