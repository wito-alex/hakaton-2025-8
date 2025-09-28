FROM python:3.12-alpine

RUN apk add --no-cache gettext

# set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# update pip
RUN pip install --upgrade pip \
    && pip install poetry

# set work directory
WORKDIR /home/backend
COPY poetry.lock pyproject.toml /home/backend/

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /home/backend
