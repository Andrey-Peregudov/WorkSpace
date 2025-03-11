from pydantic import EmailStr, BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    password_hash: str

class User(UserCreate):
    id: int

class CaseCreate(BaseModel):
    case_text: str
    data_time: datetime
    status: Optional[bool] = False
    autor_case: Optional[str] = None

class Case(CaseCreate):
    id: int