FROM python:3.12-slim

ENV POETRY_VERSION=1.7.1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY common/ common/
WORKDIR /app

COPY telegram_bot/pyproject.toml telegram_bot/poetry.lock ./
COPY telegram_bot/src/ app/

RUN poetry install --with dev

CMD ["python", "app/bot.py"]
