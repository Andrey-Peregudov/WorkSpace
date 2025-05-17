from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..model.dbbase import get_session
from ..model.models import UserDB
from ..config import key, algorithm

oauth2_scheme = HTTPBearer()

async def get_current_user(request: Request, db: AsyncSession = Depends(get_session)):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не прошел проверку подлиности")
        payload = jwt.decode(token, key, algorithms=[algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не верные данные учётной записи")
        query = select(UserDB).where(UserDB.email == email)
        result = await db.execute(query)
        db_user = result.scalars().first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователя не существует")
        return db_user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не удалось подтвердить данные",)