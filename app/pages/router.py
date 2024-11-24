from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.hotels.router import get_hotels_by_location_and_time
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
@cache(expire=30)
async def get_hotels_page(
    request: Request,
    hotels = Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )
