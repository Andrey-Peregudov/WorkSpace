from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from template_metod import templates

router = APIRouter()

templates = templates

@router.get("/converter_file", tags=["Конвертер файлов"], response_class=HTMLResponse)
def get_degree_form(request: Request):
    return templates.TemplateResponse("converter_file.html", {"request": request})

@router.get('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
@router.post('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
async def convert_dec_degree(request: Request,
                           degree_dec : float = Form(le=360)):
    try:
        degree_dec
        return templates.TemplateResponse("converter_file.html", {"request": request, "degree_dec": degree_dec})
    except ValueError:
        return templates.TemplateResponse("converter_file.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})