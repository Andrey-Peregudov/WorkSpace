from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from ..template_metod import templates

router = APIRouter()

templates = templates

@router.get("/degree_decimal", tags=["Конвертер градусов"], response_class=HTMLResponse)
def get_degree_form(request: Request):
    return templates.TemplateResponse("degree_decimal.html", {"request": request})

@router.post('/degree_decimal', response_class=HTMLResponse, summary="Перевод из десятичной системы в градусы", tags=["Конвертёр"])
async def convert_dec_degree(request: Request,
                           degree_dec : float = Form(le=360)):
    try:
        # Расчёт конвертации градусов
        grad_init = int(degree_dec)
        grad_float = float(degree_dec-grad_init)
        minute = (grad_float*60)/1
        minute =round(minute, 2)
        min_int=int(minute)
        sec=((minute-int(minute))*60)/1
        sec=round(sec, 2)
        print(f'{grad_init} + {min_int} + {sec}')
        return templates.TemplateResponse("degree_decimal.html", {"request": request, "grad_init": grad_init, "min_int": min_int, "sec": sec})
    except ValueError:
        return templates.TemplateResponse("degree_decimal.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})