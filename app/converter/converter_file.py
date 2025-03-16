from fastapi import Request, APIRouter, UploadFile
from fastapi.responses import HTMLResponse
from ..template_metod import templates

router = APIRouter()

templates = templates

@router.get("/converter_file", tags=["Конвертер файлов"], response_class=HTMLResponse)
async def get_degree_form(request: Request):
    return templates.TemplateResponse("converter_file.html", {"request": request})

@router.get('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
@router.post('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
async def create_upload_file(request: Request, file: UploadFile):
    filename = file.size
    print(filename)
    return templates.TemplateResponse("converter_file.html", {"request": request, "filename": filename})