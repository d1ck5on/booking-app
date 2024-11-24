from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, intpk
from sqlalchemy import ForeignKey


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[intpk]
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    services: Mapped[dict | None]
    quantity: Mapped[int]
    image_id: Mapped[int | None]

    hotel = relationship("Hotels", back_populates="room")
    booking = relationship("Bookings", back_populates="room")

    def __str__(self):
        return f"Room {self.name}"