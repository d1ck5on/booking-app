from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str] | None
    rooms_quantity: int
    image_id: int | None


class SHotelInfo(SHotel):
    rooms_left: int
