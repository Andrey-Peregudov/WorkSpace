from typing import Optional
from PIL import Image
from fastapi import Request, APIRouter, UploadFile, Form
from fastapi.responses import HTMLResponse
from ..template_metod import templates

router = APIRouter()

@router.get("/converter_file", tags=["Конвертер файлов"], response_class=HTMLResponse)
def get_file_convert_form(request: Request):
    return templates.TemplateResponse("converter_file.html", {"request": request})


@router.get('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
@router.post('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
async def create_upload_file(request: Request,
                       file: UploadFile,
                       conversion_type: str = Form(...)):
    try:
        filename = file.filename
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        if conversion_type == "jpeg_to_tif":
            converted_filename = filename + ".tif"
        elif conversion_type == "tif_to_jpeg":
            converted_filename = filename + ".jpg"
        elif conversion_type == "pdf_to_jpeg":
            converted_filename = filename + ".jpg"
        else:
            raise HTTPException(status_code=400, detail="Invalid conversion type")
        return templates.TemplateResponse("converter_file.html", {"request": request, "filename": filename, "converted_filename": converted_filename})

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

# from starlette.background import BackgroundTask
# # ...def cleanup():
#     os.remove(temp_file)return FileResponse(temp_file, background=BackgroundTask(cleanup),)