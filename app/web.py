import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db import get_session, init_db
from app.storage.repositories import list_coins_with_prices
from app.worker import run_worker

app = FastAPI(title="Crypto Alert Service")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def on_startup() -> None:
    init_db()
    asyncio.create_task(run_worker())


@app.get("/", response_class=HTMLResponse)
def prices_page(request: Request):
    session = get_session()
    try:
        coins = list_coins_with_prices(session)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"coins": coins},
        )
    finally:
        session.close()