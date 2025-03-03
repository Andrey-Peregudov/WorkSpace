from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

degree_page = Jinja2Templates(directory="degree/templates")

@router.get("/degree_decimal", tags=["Конвертер градусов"], response_class=HTMLResponse) # Correct tag and HTMLResponse
def get_degree_form(request: Request):
    return degree_page.TemplateResponse("degree_decimal.html", {"request": request})

@router.get('/degree_decimal', response_class=HTMLResponse, summary="Перевод из десятичной системы в градусы", tags=["Конвертёр"])
@router.post('/degree_decimal', response_class=HTMLResponse, summary="Перевод из десятичной системы в градусы", tags=["Конвертёр"]) # Renamed and updated
async def convert_dec_degree(request: Request,
                           degree_dec : float = Form(le=360)):
    try:
        grad_init = int(degree_dec)
        grad_float = float(degree_dec-grad_init)
        minute = (grad_float*60)/1
        minute =round(minute, 2)
        min_int=int(minute)
        sec=((minute-int(minute))*60)/1
        sec=round(sec, 2)
        return degree_page.TemplateResponse("degree_decimal.html", {"request": request, "grad_init": grad_init, "min_int": min_int, "sec": sec})
    except ValueError:
        return degree_page.TemplateResponse("degree_decimal.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})