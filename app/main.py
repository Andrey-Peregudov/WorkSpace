from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from template_metod import templates
from .degree import degree_function, degree_decimal_function
from .tolerances import tolerances
from .converter import converter_file
from .user_create import user_create
from .user_login import user_login


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
app.mount("/static", StaticFiles(directory="static", packages=None, html=False, check_dir=True, follow_symlink=False), name="static")

#Путь до директории templates
templates = templates

@app.get("/", tags=["Главная страница"])
def root():
    return FileResponse("templates/base.html")

@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse("404.html", {"request": request})

@app.exception_handler(422)
async def custom_422_handler(request, __):
    return templates.TemplateResponse("422.html", {"request": request})


app.include_router(degree_function.router)
app.include_router(degree_decimal_function.router)
app.include_router(tolerances.router)
app.include_router(converter_file.router)
app.include_router(user_create.router)
app.include_router(user_login.router)