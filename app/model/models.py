from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import bcrypt
from ..model.dbbase import Base


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    first_name = Column(String(80), index=True)
    last_name = Column(String(80), index=True, nullable=True)
    email = Column(String(128), unique=True, index=True)
    password_hash = Column(String(256))
    cases = relationship("CaseDB", back_populates="user")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


class CaseDB(Base):
    __tablename__ = "case"
    id = Column(Integer, primary_key=True,index=True)
    case_text = Column(String, index=True)
    data_time = Column(DateTime)
    status = Column(Boolean, nullable=True, default=False)
    autor_case = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserDB", back_populates="cases")