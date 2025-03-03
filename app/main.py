from fastapi import FastAPI, Form, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from .degree import degree_function, degree_decimal_function
from .tolerances import tolerances

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
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["Главная страница"])
def root():
    return FileResponse("templates/base.html")


app.include_router(degree_function.router)
app.include_router(degree_decimal_function.router)
app.include_router(tolerances.router)

