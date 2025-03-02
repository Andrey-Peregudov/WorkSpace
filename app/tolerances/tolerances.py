#from typing import Union
from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
import json
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

router = FastAPI(
    title="function_tolerances")


# from datetime import date
#from pydantic import BaseModel, Field

def load_tolersnces():
    try:
        with open("tolerances/tolerances.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("Ошибка: файл не существует")
        return None


@router.get('/tolerances', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
@router.post('/tolerances', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
def search_data(request: Request,
                      tolerances_class_to_find: str = Form(...),
                      size: float = Form(...)):
# @app.post('/tolerances', description="Нахождения предельных отклонений")
# def search_data(tolerances_class_to_find: str = Form(min_length=2, max_length=4, description="Поле допускка"),
#                 size: float = Form(min_length=1, max_length=4, ge=0, description="Номинальный размер")):
    global tolerances
    result = None
    if tolerances:
        for x in tolerances:
            if "tolerances_class" in x and x["tolerances_class"] == tolerances_class_to_find:

                if "upperlimit" in x and x["upperlimit"] >= size and x["lowerlimit"] <= size:
                    es_value = x.get("es")
                    ei_value = x.get("ei")

                    #Проверка что верхние и нижние отклонения not None и первый символ поля допуска в верхнем регистре
                    if es_value is not None and ei_value is not None and tolerances_class_to_find[0].isupper():
                        dmin = (size + (ei_value/1000))
                        dmax = (size + (es_value/1000))
                        result = f"Отклонения для отверстия {size}{tolerances_class_to_find}: ES = {es_value}, EI = {ei_value}, наибольший размер Dmax {dmax}мм, наименьший размер Dmin {dmin}мм"

                    # Проверка что верхние и нижние отклонения not None и первый символ поля допуска в нижнем регистре
                    elif es_value is not None and ei_value is not None and tolerances_class_to_find[0].islower():
                        dmin = (size + (ei_value/1000))
                        dmax = (size + (es_value/1000))
                        result = f"Отклонения для вала {size}{tolerances_class_to_find}: es = {es_value}, ei = {ei_value}, наибольший размер dmax {dmax}мм, наименьший размер dmin {dmin}мм"

                    else:
                        return f"Данные отсутствуют"
    return router.TemplateResponse("tolerasnces.html", {"request": request, "result": result})
