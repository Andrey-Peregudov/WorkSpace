from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from ..template_metod import templates

router = APIRouter()

templates = templates

#Конвертер градусов
@router.get("/degree", tags=["Конвертер градусов"], response_class=HTMLResponse)
def get_degree_form(request: Request):
    return templates.TemplateResponse("degree.html", {"request": request})

@router.get('/degree', response_class=HTMLResponse, summary="Перевод градусов вдесятичную систему", tags=["Конвертёр"])
@router.post('/degree', response_class=HTMLResponse, summary="Перевод градусов вдесятичную систему", tags=["Конвертёр"])
async def convert_degree(request: Request,
                           degree: int = Form(le=360),
                           minute: int = Form(le=60),
                           second: float = Form(le=60)):
    try:

        degree, minute, second = float(degree), float(minute), float(second)
        result = (degree + (minute / 60) + (second / 3600))
        result = round(result, 2)
        return templates.TemplateResponse("degree.html", {"request": request, "result": result})
    except ValueError:
        return templates.TemplateResponse("degree.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})

