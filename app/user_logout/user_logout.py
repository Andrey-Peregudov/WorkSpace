from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
from ..template_metod import templates

router = APIRouter(include_in_schema=False)

templates = templates

@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie(key="my_cookie")
    return RedirectResponse("/user_login")