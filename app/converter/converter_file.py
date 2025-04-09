from enum import nonmember
from typing import Optional
from PIL import Image
from fastapi import Request, APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from ..template_metod import templates
import os
import uuid
import io



router = APIRouter()

@router.get("/converter_file", tags=["Конвертер файлов"], response_class=HTMLResponse)
def get_file_convert_form(request: Request):
    return templates.TemplateResponse("converter_file.html", {"request": request})

UPLOAD_DIR = "image_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get('/converter_file', response_class=HTMLResponse, summary="Отображение формы", tags=["Конвертёр файлов"])
async def get_converter_form(request: Request):
    return templates.TemplateResponse("converter_file.html", {"request": request})

@router.post('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
async def create_upload_file(request: Request,
                       file: UploadFile,
                       conversion_type: str = Form(...)):
    #Проверка згружен файл
    if not file:
        raise HTTPException(status_code=400, detail="Файл не был загружен")
    try:
        #Определение формата файла.
        file_ext = file.filename.split(".")[-1].lower()
        valid_extensions = ['jpeg', 'jpg', 'tif', 'tiff', 'pdf']
        #Условие проверки формата файла согласно списка
        if file_ext not in valid_extensions:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат файла")
        #Присвоение нового уникального имени файлу
        unique_filename = f"{uuid.uuid4()}"
        print(unique_filename)
        #Путь до файла
        file_fold = os.path.join(UPLOAD_DIR, unique_filename)
        #Чтение содержимого файла
        contents = await file.read()

        #Попытка открытия изображения. Обработка ошибок
        try:
            image = Image.open(io.BytesIO(contents))
            print(f"Формат исходного файла: {image.format}")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Не удалось открыть изображение: {e}")

        #Определение формата и имени файла для сохранения на основании типа конвертации
        if conversion_type == "jpeg_to_tif":
            save_format = "TIFF"
            new_filename = f"{file_fold}.tif"
        elif conversion_type == "tif_to_jpeg":
            save_format = "JPEG"
            new_filename = f"{file_fold}.jpeg"
        else: # если не указано, в какой формат конвертировать.
            save_format = "JPEG"  # задаём значение по умолчанию.
            new_filename = f"{file_fold}.jpeg" # Имя файла по умолчанию

        # Сохранение файла
        image.save(new_filename, format=save_format)

        #Определение ответа
        return templates.TemplateResponse("converter_file.html", {
            "request": request,
            "filename": file.filename,
            "new_filename": new_filename,
            "result": f"Файл успешно сконвертирован в {save_format}" # Передаем save_format
        })

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))