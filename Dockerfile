
#### BUILDER ( Для зменшення ітогової ваги )
FROM python:3.10-alpine as builder

WORKDIR /usr/src/app/TOPUS-shop

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# psycopg2
RUN apk update --no-cache \
&& apk add postgresql-dev gcc python3-dev musl-dev \
&& pip install flake8 gunicorn

RUN pip install --upgrade pip

COPY . .

RUN flake8 \
&& pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/TOPUS-shop/wheels -r requirements.txt


#### FINAL
FROM python:3.10-alpine

ENV APP_HOME=/home/app/TOPUS-shop

# Створення дерикторій
RUN mkdir -p $APP_HOME $APP_HOME/staticfiles $APP_HOME/media $APP_HOME/media/category_photo $APP_HOME/media/cloth_photos $APP_HOME/media/gaming_photo $APP_HOME/media/home_photo $APP_HOME/media/main_photo \
&& addgroup -S app \
&& adduser -S app -G app

WORKDIR $APP_HOME

# інсталювання залежностей
COPY --from=builder /usr/src/app/TOPUS-shop/wheels /wheels
COPY --from=builder /usr/src/app/TOPUS-shop/requirements.txt .

RUN apk update \
&& apk add libpq \
&& pip install --no-cache /wheels/* \
&& chown -R app:app $APP_HOME


COPY ./entrypoint.sh .
COPY . .

USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/TOPUS-shop/entrypoint.sh"]
