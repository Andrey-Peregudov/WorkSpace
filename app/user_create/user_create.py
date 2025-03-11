from fastapi import Form, Request, APIRouter, Depends, Request, HTTPException
from ..template_metod import templates
from fastapi import status
from ..model.models import Base, UserDB, CaseDB
from sqlalchemy.ext.asyncio import AsyncSession
from ..model.dbbase import Base, get_session, engine
from ..schema.schema import UserCreate, User, CaseCreate, Case
from starlette.responses import RedirectResponse
from pydantic import EmailStr
import re

router = APIRouter()

templates = templates

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
#Создание базы данных при старте, если не создана.
# @router.on_event("startup")
# async def startup_event():
#     await create_db_and_tables()

#Страница с формой регистрации
@router.get("/user_create")
async def registration(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})


@router.post("/user_create")
async def user_create(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password_hash: str = Form(...),
    db: AsyncSession = Depends(get_session),
):
    error = []
    pattern1 = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    if re.match(pattern1, password_hash) is None:
        error.append(
            "Пароль должен быть: не менее 8-ми символов, содержать спецсимволы, заглавные и строчные буквы, цыфры"
        )
        return templates.TemplateResponse("user_create.html", {"request": request, "error": error})

    try:
        db_user = UserDB(first_name=first_name, last_name=last_name, email=email)
        db_user.set_password(password_hash)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except Exception as e:
        print(e)
        error.append("Пользователь с данной электронной почтой зарегистрирован")
        return templates.TemplateResponse("user_create.html", {"request": request, "error": error})

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)