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


@router.post("/to_do_list", response_class=HTMLResponse, summary="Список дел", tags=["Список дел"])
async def to_do(request: Request,
                db: AsyncSession = Depends(get_session),
                to_do: str = Form(...)):
    print("Роутер /to_do_list вызван")
    try:
        print("Проверка наличия токена")
        token = request.cookies.get("access_token")
        if token is None:
            print("Токен отсутствует")
            errors = ["Авторизуйтесь"]
            return templates.TemplateResponse("to_do_list.html", {"request": request, "errors": errors})

        else:
            print("Токен найден")
            shema, _, param = token.partition(" ")
            payload = jwt.decode(param, key, algorithm)
            email = payload.get("sub")

            print("Запрос пользователя из базы данных")
            result = await db.execute(select(UserDB).where(UserDB.email == email))
            user = result.scalars().first()

            if user is None:
                print("Пользователь не найден")
                errors = ["Вы не прошли аутентификацию"]
                return templates.TemplateResponse("to_do_list.html", {"request": request, "error": errors})

            else:
                print(f"Пользователь найден: {user.email}")
                print("Создание объекта CaseDB")
                new_case = CaseDB(case_text=to_do, data_time=datetime.now(), status=False,
                                  autor_case=user.id)
                print(f"Данные CaseDB: {new_case.__dict__}")
                print("Добавление объекта CaseDB в сессию")
                db.add(new_case)
                print("Коммит транзакции")
                await db.commit()
                print("Транзакция закоммичена")
                print("Обновление объекта")
                await db.refresh(new_case)
                print("Объект обновлен")

                return templates.TemplateResponse("to_do_list.html", {"request": request, "message": "Дело добавлено"})


    except Exception as e:
        print(f"Произошла ошибка: {e}")
        await db.rollback()
        errors = ["Произошла ошибка. Попробуйте позже."]
        return templates.TemplateResponse("to_do_list.html", {"request": request, "errors": errors})