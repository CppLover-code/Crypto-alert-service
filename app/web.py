import asyncio

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import get_session, init_db
from app.storage.repositories import (
    add_user,
    get_user,
    list_coins_with_prices,
    list_users,
    toggle_user_active,
    toggle_user_notify_email,
    toggle_user_notify_telegram,
)
from app.worker import run_worker

app = FastAPI(title="Crypto Alert Service")
templates = Jinja2Templates(directory="templates")


def blank_to_none(value: str) -> str | None:
    value = value.strip()
    return value if value else None

def checkbox_on(value: str | None) -> bool:
    return value == "on"

def validate_channels(
    email: str | None,
    telegram_chat_id: str | None,
    notify_email: bool,
    notify_telegram: bool,
) -> str |None:
    if notify_email and not email:
        return "Email is required when Notify email is checked."
    if notify_telegram and not telegram_chat_id:
        return "Telegram chat id is required when Notify telegram is checked."
    return None

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
        context={
            "error": None,
            "name": "",
            "email": "",
            "telegram_chat_id": "",
            "notify_email": False,
            "notify_telegram": False,
        },
    )


@app.post("/users")
def create_user(
    request: Request,
    name: str = Form(),
    email: str = Form(""),
    telegram_chat_id: str = Form(""),
    notify_email: str | None = Form(None),
    notify_telegram: str | None = Form(None),
):
    email_clean = blank_to_none(email)
    telegram_clean = blank_to_none(telegram_chat_id)
    email_on = checkbox_on(notify_email)
    telegram_on = checkbox_on(notify_telegram)

    error = validate_channels(
        email_clean, telegram_clean, email_on, telegram_on
    )
    if error:
        return templates.TemplateResponse(
            request=request,
            name="user_form.html",
            context={
                "error": error,
                "name": name,
                "email": email,
                "telegram_chat_id": telegram_chat_id,
                "notify_email": email_on,
                "notify_telegram": telegram_on,
            },
        )

    session = get_session()
    try:
        add_user(
            session,
            name=name.strip(),
            email=email_clean,
            telegram_chat_id=telegram_clean,
            notify_email=email_on,
            notify_telegram=telegram_on,
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

@app.post("/users/{user_id}/toggle-email")
def toggle_email_route(user_id: int):
    session = get_session()
    try:
        user = get_user(session, user_id)
        if user is None:
            return RedirectResponse(url="/", status_code=303)

        turning_on = not user.notify_email
        if turning_on and not user.email:
            return RedirectResponse(url="/", status_code=303)

        toggle_user_notify_email(session, user_id)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return RedirectResponse(url="/", status_code=303)

@app.post("/users/{user_id}/toggle-telegram")
def toggle_telegram_route(user_id: int):
    session = get_session()
    try:
        user = get_user(session, user_id)
        if user is None:
            return RedirectResponse(url="/", status_code=303)

        turning_on = not user.notify_telegram
        if turning_on and not user.telegram_chat_id:
            return RedirectResponse(url="/", status_code=303)

        toggle_user_notify_telegram(session, user_id)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    return RedirectResponse(url="/", status_code=303)