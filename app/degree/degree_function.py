from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

degree_page = Jinja2Templates(directory="degree/templates")

#Конвертер градусов
@router.get("/degree", tags=["Конвертер градусов"], response_class=HTMLResponse) # Correct tag and HTMLResponse
def get_degree_form(request: Request):
    return degree_page.TemplateResponse("degree.html", {"request": request})

@router.get('/degree', response_class=HTMLResponse, summary="Перевод градусов вдесятичную систему", tags=["Конвертёр"])
@router.post('/degree', response_class=HTMLResponse, summary="Перевод градусов вдесятичную систему", tags=["Конвертёр"]) # Renamed and updated
async def convert_degree(request: Request,
                           degree: int = Form(le=360),
                           minute: int = Form(le=60),
                           second: float = Form(le=60)):
    try:

        degree, minute, second = float(degree), float(minute), float(second)
        result = (degree + (minute / 60) + (second / 3600))
        result = round(result, 2)
        return degree_page.TemplateResponse("degree.html", {"request": request, "result": result})
    except ValueError:
        return degree_page.TemplateResponse("degree.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})

