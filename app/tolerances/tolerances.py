#from typing import Union
from fastapi import FastAPI, Form, Request, APIRouter
from fastapi.responses import FileResponse, HTMLResponse
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.templating import Jinja2Templates


router = APIRouter()


@router.get("/", tags=["Tolerances"])
async def get_tolerances():
    return FileResponse("templates/tolerances_page.html")

@router.get("/item/{item_id}")
async def get_tolerance_item(item_id: int):
    return {"item_id": item_id}



# tolerances_page = Jinja2Templates(directory="templates")

# #URL адрес и путь к HTML странице с шаблоном поиском отклонений
# @router.get("/tolerances", tags=["Поля допусков"])
# def root():
#     return FileResponse("templates/tolerances_page.html")

# #Функция для открытия файла json с полями допусков
# def load_tolersnces():
#     try:
#         with open("tolerances.json", "r") as f:
#             data = json.load(f)
#             return data
#     except FileNotFoundError:
#         print("Ошибка: файл не существует")
#         return None
#
# #Запуск функции сериализиции объекта Python obj в строку str формата JSON, с записью в переменную data
# tolerances = load_tolersnces()
# data = json.dumps(tolerances)


# @router.get('/tolerances', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
# @router.post('/tolerances')
# def search_data(request: Request,
#                       tolerances_class_to_find: str = Form(...),
#                       size: float = Form(...)):
#     global tolerances
#     result = None
#     if tolerances:
#         for x in tolerances:
#             if "tolerances_class" in x and x["tolerances_class"] == tolerances_class_to_find:
#
#                 if "upperlimit" in x and x["upperlimit"] >= size and x["lowerlimit"] <= size:
#                     es_value = x.get("es")
#                     ei_value = x.get("ei")
#
#                     #Проверка что верхние и нижние отклонения not None и первый символ поля допуска в верхнем регистре
#                     if es_value is not None and ei_value is not None and tolerances_class_to_find[0].isupper():
#                         dmin = (size + (ei_value/1000))
#                         dmax = (size + (es_value/1000))
#                         result = f"Отклонения для отверстия {size}{tolerances_class_to_find}"
#                         result2 = f"Верхнее отклонение:ES = {es_value}, нижнее отклонение EI = {ei_value}"
#                         result3 = f"Наибольший размер Dmax {dmax}мм, наименьший размер Dmin {dmin}мм"
#                     # Проверка что верхние и нижние отклонения not None и первый символ поля допуска в нижнем регистре
#                     elif es_value is not None and ei_value is not None and tolerances_class_to_find[0].islower():
#                         dmin = (size + (ei_value/1000))
#                         dmax = (size + (es_value/1000))
#                         result = f"Отклонения для вала {size}{tolerances_class_to_find}"
#                         print(result)
#                         result2 = f"Верхнее отклонение: es = {es_value}, нижнее отклонение ei = {ei_value}"
#                         print(result2)
#                         result3 = f"Наибольший размер dmax {dmax}мм, наименьший размер dmin {dmin}мм"
#                         print(result3)
#                     else:
#                         return f"Данные отсутствуют"
#     return tolerances_page.TemplateResponse("tolerances_page.html", {"request": request, "result": result, "result2":result2, "result3":result3})

