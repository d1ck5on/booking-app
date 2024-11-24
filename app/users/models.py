from sqlalchemy.orm import Mapped, relationship
from app.database import Base, intpk


class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str]
    hashed_password: Mapped[str]

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"User {self.email}"
