FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
COPY ./interview_tg_bot /app

WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install /tmp/requirements.txt


ENV PATH="/scripts:/py/bin:$PATH"