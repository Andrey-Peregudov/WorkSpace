#from typing import Union
from fastapi import FastAPI, Form, UploadFile, Request, APIRouter
from fastapi.responses import FileResponse, HTMLResponse
import json
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
# from datetime import date
#from pydantic import BaseModel, Field


router = APIRouter()


@router.get('/tolerances', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
@router.post('/tolerances')
def search_data(request: Request,
                      degree: int = Form(...),
                      minute: float = Form(...),
                      second: float = Form(...)):

# Функция перевода градусов в дясятичную систему
def grad_to_dec(a:int,b:int,c:int):
    result = (a+(b/60)+(c/360))
    result = round(result, 2)
    return result

a=grad_to_dec(54,35,24)
print(a)


# Функция перевода градусов из десятичной системы
def dec_to_grad(grad):
    grad_init = int(grad)
    grad_float = float(grad-grad_init)
    min = (grad_float*60)/1
    min=round(min, 2)
    min_int=int(min)
    sec=((min-int(min))*60)/1
    sec=round(sec, 2)
    return f"Градусы {grad_init} Минуты {min_int} Секунды {sec}"