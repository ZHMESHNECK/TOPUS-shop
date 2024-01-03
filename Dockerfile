#### BUILDER ( Для зменшення ітогової ваги )

FROM python:3.10-alpine as builder

WORKDIR /TOPUS-shop

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
RUN pip install flake8
COPY . .
RUN flake8 --ignore=E501,F811,F405,F401,E241,E231 .

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#### FINAL
FROM python:3.10-alpine

RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app

# Створення дерикторій
ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir %APP_HOME
WORKDIR %APP_HOME

# інсталювання залежностей
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh %APP_HOME
COPY . %APP_HOME

RUN chown -R app:app %APP_HOME

USER app

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD [ "gunicorn", "--config", "gunicorn_config.py", "TOPUS.wsgi:application" ]