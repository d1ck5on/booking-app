from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from sqladmin import Admin, ModelView
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.config import settings

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import get_rooms

from app.pages.router import router as router_pages
from app.images.router import router as router_images

from app.database import engine

from app.admin.auth import authentication_backend


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_bookings)
app.include_router(router_users)
app.include_router(router_hotels)

app.include_router(router_pages)
app.include_router(router_images)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)
