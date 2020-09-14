from fastapi import Depends, FastAPI, Header, HTTPException

from datetime import datetime, timedelta
from pydantic import BaseModel

from starlette.staticfiles import StaticFiles

# Add support for static swagger
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from starlette.requests import Request
from starlette.responses import HTMLResponse

from routers import pb_pyscripts, pb_atv

app = FastAPI(docs_url=None, redoc_url=None)
app.mount("/python_scripts", StaticFiles(directory="python_scripts"))
app.mount("/static", StaticFiles(directory="static"))


@app.get("/")
async def read_main():
    return "For Usage:/scripts/upload_file : To upload file, /execute_script/{filename}{function}{arguments} : Adhoc running of script, /atv/---POST([treats events JSON, rule YML]) : Parse yml to steps, iterate through steps with treats events and output status"

app.include_router(pb_pyscripts.router)
app.include_router(pb_atv.router)

@app.get("/healthz", tags=["kubernetes"])
async def return_health():
    return str(datetime.now())


####################################################
# Function to serve offline swagger and static files
####################################################
async def swagger_ui_html(req: Request) -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + ' - Swagger UI',
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url='/static/swagger-ui-bundle.js',
        swagger_css_url='/static/swagger-ui.css',
    )

app.add_route('/docs', swagger_ui_html, include_in_schema=False)

if app.swagger_ui_oauth2_redirect_url:
    async def swagger_ui_redirect(req: Request) -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    app.add_route(
        app.swagger_ui_oauth2_redirect_url,
        swagger_ui_redirect,
        include_in_schema=False
    )


async def redoc_html(req: Request) -> HTMLResponse:
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + ' - ReDoc',
        redoc_js_url='/static/redoc.standalone.js',
    )

app.add_route('/redoc', redoc_html, include_in_schema=False)
