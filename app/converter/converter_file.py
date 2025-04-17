from PIL import Image
from fastapi import Request, APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from ..template_metod import templates
import os
import uuid
import io
from shutil import rmtree

router = APIRouter()

# @router.get("/converter_file", tags=["Конвертер файлов"], response_class=HTMLResponse)
# def get_file_convert_form(request: Request):
#     return templates.TemplateResponse("converter_file.html", {"request": request})

UPLOAD_DIR = "image_data"
MAX_DIR_SIZE_MB = 1024 # Максимальный размер папки в мегабайтах (1GB)
MAX_FILE_AGE_SECONDS = 3600 # Максимальный возраст файла в секундах (1 час)




@router.get('/converter_file', response_class=HTMLResponse, summary="Отображение формы", tags=["Конвертёр файлов"])
async def get_converter_form(request: Request):
    return templates.TemplateResponse("converter_file.html", {"request": request})

@router.post('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
async def create_upload_file(request: Request,
                       file: UploadFile,
                       conversion_type: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Файл не был загружен")
    try:
        file_ext = file.filename.split(".")[-1].lower()
        valid_extensions = ['jpeg', 'jpg', 'tif', 'tiff', 'pdf']
        if file_ext not in valid_extensions:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")

        unique_filename = str(uuid.uuid4())
        file_fold = os.path.join(UPLOAD_DIR, unique_filename)
        contents = await file.read()

        try:
            image = Image.open(io.BytesIO(contents))
            print(f"Формат исходного файла: {image.format}, Размер: {len(contents)} байт")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Не удалось открыть изображение: {e}")

        if conversion_type == "jpeg_to_tif":
            save_format = "TIFF"
            new_filename = f"{file_fold}.tif"
            download_filename = f"{unique_filename}.tif"
        elif conversion_type == "tif_to_jpeg":
            save_format = "JPEG"
            new_filename = f"{file_fold}.jpeg"
            download_filename = f"{unique_filename}..jpeg"
        else:
            save_format = "JPEG"
            new_filename = f"{file_fold}.jpeg"
            download_filename = f"{unique_filename}.jpeg"

        try:
            if save_format == "TIFF":
                image.save(new_filename, format=save_format, compression="none")
            else:
                image.save(new_filename, format=save_format, quality=100)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {e}")

        saved_file_size = os.path.getsize(new_filename)
        print(f"Размер сохранённого файла: {saved_file_size} байт")

        # Возвращаем FileResponse для скачивания
        return FileResponse(
            new_filename,
            media_type="image/tiff" if save_format == "TIFF" else "image/jpeg",
            filename=download_filename
        )


    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))