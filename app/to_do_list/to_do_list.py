from turtledemo.sorting_animate import partition
from fastapi import Form, Request, APIRouter
from fastapi.responses import HTMLResponse
from ..template_metod import templates
from jose import jwt
from ..config import key, algorithm
from ..model.dbbase import Base, get_session, engine
from ..model.models import UserDB, CaseDB


router = APIRouter()

@router.get("/to_do_list", tags=["Конвертер градусов"], response_class=HTMLResponse)
def to_do_page(request: Request):
    return templates.TemplateResponse("to_do_list.html", {"request": request})

@router.get("/to_do_list", response_class=HTMLResponse, summary="Список дел", tags=["Список дел"])
@router.post("/to_do_list", response_class=HTMLResponse, summary="Список дел", tags=["Список дел"])
async def to_do(request: Request,
                db: AsyncSession = Depends(get_session),
                to_do: str = Form(str)):
    errors = []
    try:
        token = request.cookies.get("access_token")
        if token is None:
            errors.append("Авторизуйтесь")
            return templates.TemplateResponse("to_do_list.html", {"request": request, "errors":errors})
        else:
            shema,_, param = token,partition(" ")
            payload = jwt.decode(param, key, algorithm)
            email = payload.get("sub")
            user = db.query(UserDB).filter(UserDB.email==email).first()
            if user is None:
                errors.append("Вы не прошли аутентификацию")
                return templates.TemplateResponse("to_do_list.html", {"request": request, "error": errors})
    except ValueError:
        return templates.TemplateResponse("to_do_list.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})