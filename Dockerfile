FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1

COPY ./interview_tg_bot /app
COPY requirements.txt /tmp/requirements.txt

WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt


ENV PATH="/scripts:/py/bin:$PATH"