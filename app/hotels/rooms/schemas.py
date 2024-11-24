from pydantic import BaseModel


class SRoomCropped(BaseModel):
    image_id: int | None
    name: str
    description: str | None
    services: list | None


class SRoom(SRoomCropped):
    id: int
    hotel_id: int
    price: int
    quantity: int


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int
