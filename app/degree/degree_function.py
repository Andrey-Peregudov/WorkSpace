from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from ..template_metod import templates
from typing import Optional

router = APIRouter()

templates = templates

#Конвертер градусов
@router.get("/degree", tags=["Конвертер градусов"], response_class=HTMLResponse)
def get_degree_form(request: Request):
    return templates.TemplateResponse("degree.html", {"request": request})

@router.post('/degree', response_class=HTMLResponse, summary="Перевод градусов вдесятичную систему", tags=["Конвертёр"])
async def convert_degree(request: Request,
                           degree: int = Form(default=0, le=360),
                           minute: Optional[int] = Form(default=0, le=60),
                           second: Optional[float] = Form(default=0.0, le=60)):
    try:
        # Расчёт конвертации градусов
        degree, minute, second = float(degree), float(minute), float(second)
        result = (degree + (minute / 60) + (second / 3600))
        result = round(result, 2)
        return templates.TemplateResponse("degree.html", {"request": request, "result": result})
    except ValueError:
        return templates.TemplateResponse("degree.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})

