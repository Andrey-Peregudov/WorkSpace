from enum import nonmember
from typing import Optional
from PIL import Image
from fastapi import Request, APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
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

@router.get('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
@router.post('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
async def create_upload_file(request: Request,
                       file: UploadFile,
                       conversion_type: str = Form(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Файл не был загружен")
    file_exp = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}"
    file_fold = os.path.join(UPLOAD_DIR, unique_filename)

    contents = await file.read()
    image = Image.open(io.BytesIO(contents))


    if conversion_type == "jpeg_to_tif":
        save_format = "TIFF"
        new_filename = f"{file_fold}.tif"
    elif conversion_type == "tif_to_jpeg":
        save_format = "JPEG"
        new_filename = f"{file_fold}.jpeg"
    elif conversion_type == "pdf_to_jpeg":
        save_format = "JPEG"
        new_filename = f"{file_fold}.jpeg"
    else:
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип конвертации")

    image.save(new_filename, format=save_format)

    return templates.TemplateResponse("converter_file.html", {
        "request": request,
        "filename": file.filename,
        "file_fold": new_filename,
        "result": f"Файл успешно сконвертирован в {save_format}"
    })



    # if jpeg_to_tif:
    #     result = 1
    # elif tif_to_jpeg:
    #     result = 2
    # elif pdf_to_jpeg:
    #     result = 3
    # else:
    #     result = 'Повторите действие'
    return templates.TemplateResponse("converter_file.html", {"request": request, "file":file})

        # fiel_path = ".image_data"
        # filename = file.filename
        # image = Image.open(file).save(fiel_path)
        # print(filename)
        # contents = await file.read()
        # image = Image.open(io.BytesIO(contents))
        # if conversion_type == "jpeg_to_tif":
        #     converted_filename = filename + ".tif"
        # elif conversion_type == "tif_to_jpeg":
        #     converted_filename = filename + ".jpg"
        # elif conversion_type == "pdf_to_jpeg":
        #     converted_filename = filename + ".jpg"
        # else:
    #     if not file:
    #         return {"message": "No upload file sent"}
    #     else:
    #         return {"filename": file.filename}
    #     return templates.TemplateResponse("converter_file.html", {"request": request, "filename": filename, "converted_filename": converted_filename})
    #
    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=500, detail=str(e))

# from starlette.background import BackgroundTask
# # ...def cleanup():
#     os.remove(temp_file)return FileResponse(temp_file, background=BackgroundTask(cleanup),)