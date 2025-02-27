#from typing import Union
from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
import json
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
# from datetime import date
#from pydantic import BaseModel, Field

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]


app = FastAPI(
    middleware=middleware,
    title="WorkSpace")
#Путь до директории static
#app.mount("/static", StaticFiles(directory="static", html=True), name="static")
app.mount("/static", StaticFiles(directory="static", packages=None, html=False, check_dir=True, follow_symlink=False))
#Путь до директории templates
templates = Jinja2Templates(directory="templates")
tolerances_page = Jinja2Templates(directory="tolerances/templates")

# #Переменная для хранения сегодняшней даты
# a = date.today()

#Функция для открытия файла json с полями допусков
def load_tolersnces():
    try:
        with open("tolerances/tolerances.json", "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("Ошибка: файл не существует")
        return None

#Запуск функции сериализиции объекта Python obj в строку str формата JSON, с записью в переменную data
tolerances = load_tolersnces()
data = json.dumps(tolerances)

#pydentic модели проверки данных
# class Base(BaseModel):
#     pass

# class TolerancesSchema(Base):
#     tolerances_class_to_find: str = Field(min_length=2 ,max_length=4, description="Поле допускка")
#     size: float = Field(min_length=1, max_length=4, ge=0, description="Номинальный размер")


@app.get("/", tags=["Главная страница"])
def root():
    return FileResponse("templates/base.html")
@app.get("/tolerances", tags=["Поля допусков"])
def root():
    return FileResponse("tolerances/templates/tolerances_page.html")


@app.get('/tolerances', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
@app.post('/tolerances')
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
                        result = f"Отклонения для отверстия {size}{tolerances_class_to_find}"
                        result2 = f"Верхнее отклонение:ES = {es_value}, нижнее отклонение EI = {ei_value}"
                        result3 = f"Наибольший размер Dmax {dmax}мм, наименьший размер Dmin {dmin}мм"
                    # Проверка что верхние и нижние отклонения not None и первый символ поля допуска в нижнем регистре
                    elif es_value is not None and ei_value is not None and tolerances_class_to_find[0].islower():
                        dmin = (size + (ei_value/1000))
                        dmax = (size + (es_value/1000))
                        result = f"Отклонения для вала {size}{tolerances_class_to_find}"
                        result2 = f"Верхнее отклонение: es = {es_value}, нижнее отклонение ei = {ei_value}"
                        result3 = f"Наибольший размер dmax {dmax}мм, наименьший размер dmin {dmin}мм"
                    else:
                        return f"Данные отсутствуют"
    return tolerances_page.TemplateResponse("tolerances_page.html", {"request": request, "result": result, "result2":result2, "result3":result3})



import angle

app.include_router(angle.router, tags=["Users | angle.py"], prefix="/api")



#search_data("H7",180)

# @app.route("/tolerances")
# async def tolerances(search_data("H7",180)):
#     return




# # Функция перевода градусов в дясятичную систему
# def grad_to_dec(a:int,b:int,c:int):
#     result = (a+(b/60)+(c/360))
#     result = round(result, 2)
#     return result
#
# a=grad_to_dec(54,35,24)
# print(a)


# # Функция перевода градусов из десятичной системы
# def dec_to_grad(grad):
#     grad_init = int(grad)
#     grad_float = float(grad-grad_init)
#     min = (grad_float*60)/1
#     min=round(min, 2)
#     min_int=int(min)
#     sec=((min-int(min))*60)/1
#     sec=round(sec, 2)
#     return f"Градусы {grad_init} Минуты {min_int} Секунды {sec}"


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True, host="0.0.0.0")
#
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}