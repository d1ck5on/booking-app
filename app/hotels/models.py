from sqlalchemy.orm import Mapped, relationship
from app.database import Base, intpk


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[intpk]
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[dict | None]
    rooms_quantity: Mapped[int]
    image_id: Mapped[int | None]

    room = relationship("Rooms", back_populates="hotel")

    def __str__(self):
        return f"Hotel {self.name} {self.location[:30]}"
