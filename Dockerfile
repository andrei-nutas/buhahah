FROM python:3.13.2-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app.

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./
COPY . ./

RUN poetry config virtualenvs.create true

RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "all-api-tests"]