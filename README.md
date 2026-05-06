🇬🇧 English

# Crypto Alert Service

Crypto Alert Service is an asynchronous cryptocurrency monitoring application built with Python.

The service tracks cryptocurrency prices using the CoinGecko REST API and sends alerts via Telegram and Email when specified conditions are met.

## Features

* Async REST API client (`aiohttp`)
* Cryptocurrency price monitoring
* Configurable alerts system
* Telegram notifications
* Email notifications (Gmail SMTP)
* Anti-spam alerts logic
* Persistent alerts state
* Logging system
* JSON storage
* Docker support
* Environment variables support (`.env`)
* Adaptive polling for API rate limits
* Production-style project architecture

## Supported Cryptocurrencies

You can monitor any cryptocurrency supported by CoinGecko API.

Example:

* Bitcoin (BTC)
* Ethereum (ETH)
* Litecoin (LTC)
* Celestia (TIA)

## Technologies Used

* Python 3.13
* Asyncio
* Aiohttp
* Docker
* SMTP
* Telegram Bot API

## Project Structure

```text
app/
├── api/
├── services/
├── storage/
├── utils/
├── config.py
├── main.py
```

## Installation

### Clone repository

```bash
git clone <your_repo_url>
cd crypto-alert-service
```

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create `.env` file in the project root:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Run Application

```bash
python -m app.main
```

## Run with Docker

### Build image

```bash
docker build -t crypto-alert-service .
```

### Run container

```bash
docker run --env-file .env crypto-alert-service
```

## Alerts Example

```text
🚨 ₿ BTC price ABOVE 100000.00

Current price BTC: 81466.37 USD
```

## Future Improvements

* Windows background service
* Installer (.exe)
* Database support
* Web dashboard
* WebSocket real-time updates
* FastAPI integration

## License

MIT License

# ---------------------------------------------------------------
🇷🇺 Русский

Crypto Alert Service

Crypto Alert Service — асинхронное приложение для мониторинга криптовалют, написанное на Python.

Сервис отслеживает цены криптовалют через REST API CoinGecko и отправляет уведомления в Telegram и Email при выполнении заданных условий.

Возможности
Асинхронный REST API клиент (aiohttp)
Мониторинг цен криптовалют
Гибкая система алертов
Telegram уведомления
Email уведомления (Gmail SMTP)
Anti-spam логика для алертов
Сохранение состояния алертов
Система логирования
Сохранение данных в JSON
Поддержка Docker
Поддержка .env
Adaptive polling при API rate limits
Архитектура в стиле production backend
Поддерживаемые криптовалюты

Можно отслеживать любые криптовалюты, поддерживаемые CoinGecko API.

Примеры:

Bitcoin (BTC)
Ethereum (ETH)
Litecoin (LTC)
Celestia (TIA)
Используемые технологии
Python 3.13
Asyncio
Aiohttp
Docker
SMTP
Telegram Bot API
Структура проекта
app/
├── api/
├── services/
├── storage/
├── utils/
├── config.py
├── main.py
Установка
Клонирование репозитория
git clone <your_repo_url>
cd crypto-alert-service
Создание виртуального окружения
python -m venv .venv
Активация виртуального окружения

Windows:

.venv\Scripts\activate

Linux/macOS:

source .venv/bin/activate
Установка зависимостей
pip install -r requirements.txt
Переменные окружения

Создайте .env файл в корне проекта:

EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
Запуск приложения
python -m app.main
Запуск через Docker
Сборка Docker image
docker build -t crypto-alert-service .
Запуск контейнера
docker run --env-file .env crypto-alert-service
Пример уведомления
🚨 ₿ BTC price ABOVE 100000.00

Current price BTC: 81466.37 USD
Возможные улучшения
Windows background service
Installer (.exe)
Поддержка базы данных
Web dashboard
WebSocket real-time updates
Интеграция FastAPI
Лицензия

MIT License