from fastapi import Form, Request, APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from ..template_metod import templates
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.models import UserDB
from ..model.dbbase import get_session
from sqlalchemy import select
from jose import jwt
from ..config import key, algorithm

router = APIRouter(include_in_schema=False)

templates = templates

@router.get("/user_login")
async def registration(request: Request):
    return templates.TemplateResponse("user_login.html", {"request": request})

@router.post("/user_login")
async def user_create(
    response: Response,
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_session)):
    # Пустой список ошибок
    error = []
    try:
        # Запрос к БД столбец email
        query = select(UserDB).where(UserDB.email == email)
        # Выполняется асинхронный запрос к БД
        result = await db.execute(query)
        # Получение первого совпавшего объекта
        db_user = result.scalars().first()

        if db_user is None:
            error.append("Такого пользователя нет")
            return templates.TemplateResponse("user_login.html", {"request": request, "error": error})
        else:
            # Получение JWT
            if db_user.check_password(password):
                jwt_token = jwt.encode(claims={"sub":email}, key=key, algorithm = algorithm)
                response.set_cookie(key="access_token", value=jwt_token, httponly=True)
                message = "Вы успешно вошли в систему"
                response = templates.TemplateResponse("base.html", {"request": request, "message": message})
                response.set_cookie(key="access_token", value=jwt_token, httponly=True)
                return response
            else:
                error.append("Неверный пароль")
                return templates.TemplateResponse("user_login.html", {"request": request, "error": error})
    except Exception as e:
        print(e)
        error.append("Ошибка при входе")
        return templates.TemplateResponse("user_login.html", {"request": request, "error": error})