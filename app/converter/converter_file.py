from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

converter_file = Jinja2Templates(directory="templates")

@router.get("/converter_file", tags=["Конвертер файлов"], response_class=HTMLResponse)
def get_degree_form(request: Request):
    return converter_file.TemplateResponse("converter_file.html", {"request": request})

@router.get('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
@router.post('/converter_file', response_class=HTMLResponse, summary="Конвертация файлов", tags=["Конвертёр файлов"])
async def convert_dec_degree(request: Request,
                           degree_dec : float = Form(le=360)):
    try:
        degree_dec
        return converter_file.TemplateResponse("converter_file.html", {"request": request, "degree_dec": degree_dec})
    except ValueError:
        return converter_file.TemplateResponse("converter_file.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})