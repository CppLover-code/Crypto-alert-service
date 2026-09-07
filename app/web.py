import asyncio

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import get_session, init_db
from app.storage.repositories import (
    add_user,
    deactivate_user,
    list_coins_with_prices,
    list_users,
    toggle_user_active,
)
from app.worker import run_worker

app = FastAPI(title="Crypto Alert Service")
templates = Jinja2Templates(directory="templates")


def blank_to_none(value: str) -> str | None:
    value = value.strip()
    return value if value else None


@app.on_event("startup")
async def on_startup() -> None:
    init_db()
    asyncio.create_task(run_worker())


@app.get("/", response_class=HTMLResponse)
def prices_page(request: Request):
    session = get_session()
    try:
        coins = list_coins_with_prices(session)
        users = list_users(session)
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"coins": coins, "users": users},
        )
    finally:
        session.close()


@app.get("/users/new", response_class=HTMLResponse)
def new_user_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="user_form.html",
        context={},
    )


@app.post("/users")
def create_user(
    name: str = Form(),
    email: str = Form(""),
    telegram_chat_id: str = Form(""),
):
    session = get_session()
    try:
        add_user(
            session,
            name=name.strip(),
            email=blank_to_none(email),
            telegram_chat_id=blank_to_none(telegram_chat_id),
        )
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return RedirectResponse(url="/", status_code=303)

@app.post("/users/{user_id}/toggle-active")
def toggle_user_active_route(user_id: int):
    session = get_session()
    try:
        toggle_user_active(session, user_id)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return RedirectResponse(url="/", status_code=303)