from fastapi import UploadFile, APIRouter
import shutil

from app.tasks.tasks import process_pic


router = APIRouter(
    prefix="/images",
    tags=["Uploading images"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
    process_pic.delay(im_path)
