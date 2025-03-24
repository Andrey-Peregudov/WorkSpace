from fastapi import Form, Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
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
                to_do: str = Form(...)):
    errors = []
    try:
        token = request.cookies.get("access_token")
        if token is None:
            errors.append("Авторизуйтесь")
            return templates.TemplateResponse("to_do_list.html", {"request": request, "errors":errors})
        else:
            shema,_, param = token.partition(" ")
            payload = jwt.decode(param, key, algorithm)
            email = payload.get("sub")
            user = db.query(UserDB).filter(UserDB.email==email).first()
            if user is None:
                errors.append("Вы не прошли аутентификацию")
                return templates.TemplateResponse("to_do_list.html", {"request": request, "error": errors})
            else:
                item = CaseDB(case_text=to_do, data_time=datetime.now(), status=False, autor_case=user.id)
                db.add(item)
                await db.commit()
                await db.refresh(item)
                return templates.TemplateResponse("to_do_list.html", {"request": request, "message": "Дело добавлено"})
    except ValueError:
        return templates.TemplateResponse("to_do_list.html", {"request": request, "error": "Ошибка ввода. Введите значения заново"})
