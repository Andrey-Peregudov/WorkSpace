from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
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
app.mount("/static", StaticFiles(directory="static", packages=None, html=False, check_dir=True, follow_symlink=False), name="static")
#Путь до директории templates
templates = Jinja2Templates(directory="templates")
tolerances_page = Jinja2Templates(directory="tolerances/templates")

# #Переменная для хранения сегодняшней даты
# a = date.today()

#Функция для открытия файла json с полями допусков
# def load_tolersnces():
#     try:
#         with open("tolerances/tolerances.json", "r") as f:
#             data = json.load(f)
#             return data
#     except FileNotFoundError:
#         print("Ошибка: файл не существует")
#         return None
#
# #Запуск функции сериализиции объекта Python obj в строку str формата JSON, с записью в переменную data
# tolerances = load_tolersnces()
# data = json.dumps(tolerances)

#pydentic модели проверки данных
# class Base(BaseModel):
#     pass

# class TolerancesSchema(Base):
#     tolerances_class_to_find: str = Field(min_length=2 ,max_length=4, description="Поле допускка")
#     size: float = Field(min_length=1, max_length=4, ge=0, description="Номинальный размер")

#URL адрес и путь к HTML странице с шаблоном главной страницы




@app.get("/", tags=["Главная страница"])
def root():
    return FileResponse("templates/base.html")


#Функция поиска отклонений по полю допуска
# @app.get('/tolerances', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
# @app.post('/tolerances')
# def search_data(request: Request,
#                       tolerances_class_to_find: str = Form(...),
#                       size: float = Form(...)):
# # @app.post('/tolerances', description="Нахождения предельных отклонений")
# # def search_data(tolerances_class_to_find: str = Form(min_length=2, max_length=4, description="Поле допускка"),
# #                 size: float = Form(min_length=1, max_length=4, ge=0, description="Номинальный размер")):
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
#                         result2 = f"Верхнее отклонение: es = {es_value}, нижнее отклонение ei = {ei_value}"
#                         result3 = f"Наибольший размер dmax {dmax}мм, наименьший размер dmin {dmin}мм"
#                     else:
#                         return f"Данные отсутствуют"
#     return tolerances_page.TemplateResponse("tolerances_page.html", {"request": request, "result": result, "result2":result2, "result3":result3})


# #Функция переода грдусов в десятичную систему
# # @app.get('/angle', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
# @app.post('/angle', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
# def search_data(request: Request,
#                       degree: str = Form(...),
#                       minute: str = Form(...),
#                       second: str = Form(...)):
#     degree, minute, second = float(degree), float(minute), float(second)
#     result = (degree+(minute/60)+(second/3600))
#     result = round(result, 2)
#     return angle_page.TemplateResponse("angle.html", {"request": request, "result": result})
#
#
# # @app.get('/angle2', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
# @app.post('/angle2', response_class=HTMLResponse, summary="Нахождение предельных отклонений", tags=["Поля допусков"])
# def search_data(request: Request,
#                       degree_decimal: str = Form(...)):
#     degree_decimal = float(degree_decimal)
#     #Перевод из дестичной системы в градусы минуты секунды
#     deg_init = int(degree_decimal)
#     deg_float = float(degree_decimal-deg_init)
#     minutes = (deg_float*60)/1
#     minutes = round(min, 2)
#     min_int=int(minutes)
#     sec=((minutes-min_int)*60)/1
#     sec=round(sec, 2)
#     return angle_page.TemplateResponse("degree_decimal.html", {"request": request, "deg_init": deg_init, "min_int": min_int, "sec": sec})


app.include_router(degree_function.router)

