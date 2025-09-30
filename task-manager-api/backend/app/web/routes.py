from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request, "title": "Tasks"})


@router.get("/docs-page", response_class=HTMLResponse)
async def docs_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("docs.html", {"request": request, "title": "API Docs"})


