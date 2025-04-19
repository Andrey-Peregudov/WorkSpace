from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from template_metod import templates
from .degree import degree_function, degree_decimal_function
from .tolerances import tolerances
from .converter import converter_file
from .user_create import user_create
from .user_login import user_login
from .to_do_list import to_do_list

# Функции которые выполняются для каждого запроса, перед выполнением endpoint
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

# Экземляр приложения FastAPI
app = FastAPI(
    middleware=middleware,
    title="WorkSpace",
    docs_url=None,
    redoc_url=None)

# Подключение к директории static
app.mount("/static", StaticFiles(directory="static", packages=None, html=False, check_dir=True, follow_symlink=False), name="static")

# Шаблон главной страницы
@app.get("/")
async def info(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})

# Шаблон банера ошибки 400 Bad Request
@app.exception_handler(400)
async def custom_400_handler(request, __):
    return templates.TemplateResponse("400.html", {"request": request})

# Шаблон банера ошибки 401 Unauthorized
@app.exception_handler(401)
async def custom_401_handler(request, __):
    return templates.TemplateResponse("401.html", {"request": request})

# Шаблон банера ошибки 403 Forbidden
@app.exception_handler(403)
async def custom_403_handler(request, __):
    return templates.TemplateResponse("403.html", {"request": request})

# Шаблон банера ошибки 404 Not Found
@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request})

# Шаблон банера ошибки 422 Unprocessable Entity
@app.exception_handler(RequestValidationError)
async def custom_422_handler(request, __):
    return templates.TemplateResponse("422.html", {"request": request})

# Шаблон банера ошибки 500 Internal Server Error
@app.exception_handler(500)
async def custom_500_handler(request, __):
    return templates.TemplateResponse("500.html", {"request": request})

# Шаблон банера ошибки 501 Not Implemented
@app.exception_handler(501) 
async def custom_501_handler(request, __):
    return templates.TemplateResponse("501.html", {"request": request})

# Подключение маршрутов разлиных функций
app.include_router(degree_function.router)
app.include_router(degree_decimal_function.router)
app.include_router(tolerances.router)
app.include_router(converter_file.router)
app.include_router(user_create.router)
app.include_router(user_login.router)
app.include_router(to_do_list.router)