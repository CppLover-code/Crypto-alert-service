# Crypto Alert Service

Async Python service that polls [CoinGecko](https://www.coingecko.com/) for crypto prices and sends alerts over Telegram and email when configured thresholds are crossed.

An admin page shows live prices and lets you add subscribers. Subscribers do not log in: they only receive messages.

---

## Stack

- Python 3.13, asyncio, aiohttp
- FastAPI + Jinja2 (admin UI)
- SQLite + SQLAlchemy
- Telegram Bot API, Gmail SMTP
- Docker Compose
- pytest

---

## How it works

1. A background worker fetches prices on an interval (`config/config.json`).
2. Prices are stored in SQLite (`data/app.db`) and shown on `/`.
3. If a coin crosses an `above` / `below` threshold, the worker notifies **active** users according to their Email / Telegram flags.
4. Alert state is persisted so the same condition does not spam until the price leaves the range and enters it again.

**Server secrets** (SMTP login, bot token) live in `.env`.  
**Recipients** (email, Telegram chat id, channel toggles) live in the admin UI / database.

`notifications.*.enabled` in `config.json` means “this channel is available on the server”. Per-user checkboxes decide who actually receives a message.

---

## Setup

```bash
git clone https://github.com/CppLover-code/Crypto-alert-service.git
cd Crypto-alert-service
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux / macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` in the project root:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
TELEGRAM_TOKEN=your_telegram_bot_token
```

Gmail needs an [app password](https://support.google.com/accounts/answer/185833), not the normal account password.  
Telegram: create a bot via [@BotFather](https://t.me/BotFather), then the subscriber must send `/start` to the bot before it can message them. Chat id is entered in the admin form, not in `.env`.

Thresholds and coins: `config/config.json`.

---

## Run locally

From the project root (port 8080 — port 8000 is often blocked on Windows):

```bash
uvicorn app.web:app --reload --port 8080
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080).

This starts both the admin UI and the polling worker. Do not run `python -m app.main` at the same time or you will double-poll the API.

Worker only (no UI):

```bash
python -m app.main
```

---

## Run with Docker

Docker Desktop must be running. From the project root:

```bash
docker compose up --build
```

Then open [http://127.0.0.1:8080](http://127.0.0.1:8080).

SQLite, logs, and config are mounted from `./data`, `./logs`, and `./config`, so they survive `docker compose down`.

Stop: `Ctrl+C`. Remove the container (data on disk stays): `docker compose down`.

---

## Tests

```bash
pytest -q
```

No network, Telegram, or Gmail required.

---

## Alert example

```text
🚨 ₿ BTC price ABOVE 100000.00

Current price BTC: 81466.37 USD
```

---

## Possible next steps

- Subscriber self-service via Telegram commands
- Per-user alert thresholds
- Auth on the admin page

---

## License

MIT License

---

# Русский

Сервис на Python, который по таймеру запрашивает цены криптовалют у CoinGecko и шлёт алерты в Telegram и на почту, когда цена пересекает порог из конфига.

Админ-страница показывает текущие цены и список подписчиков. Подписчики на сайт не заходят — только получают сообщения.

## Стек

Python 3.13, asyncio, aiohttp, FastAPI, Jinja2, SQLite, SQLAlchemy, Telegram Bot API, Gmail SMTP, Docker Compose, pytest.

## Как устроено

Воркер опрашивает API, пишет цены в SQLite и рисует их на `/`. При срабатывании порога сообщения уходят **активным** пользователям по их флагам Email / Telegram. Состояние алертов сохраняется, чтобы не спамить, пока цена снова не выйдет из условия.

Секреты отправителя — в `.env`. Получатели — в админке.  
`enabled` в `config.json` — «сервер умеет этот канал»; галки на пользователе — «этому человеку слать».

## Запуск

```bash
git clone https://github.com/CppLover-code/Crypto-alert-service.git
cd Crypto-alert-service
```

Скопируйте `.env.example` в `.env`, заполните `EMAIL_USER`, `EMAIL_PASSWORD` (пароль приложения Gmail) и `TELEGRAM_TOKEN`. Chat id подписчика указывается в форме Add user; человек должен один раз написать боту `/start`.

Локально (из корня проекта):

```bash
uvicorn app.web:app --reload --port 8080
```

Админка: http://127.0.0.1:8080  
Не запускайте параллельно `python -m app.main`.

Docker:

```bash
docker compose up --build
```

Тесты: `pytest -q`

## Лицензия

MIT License
