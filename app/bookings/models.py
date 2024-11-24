from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, intpk
from datetime import date


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[intpk]
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int]
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))

    user = relationship("Users", back_populates="booking")
    room = relationship("Rooms", back_populates="booking")

    def __str__(self):
        return f"Booking #{self.id}"
