FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

LABEL maintainer="Maurice Koster <mauricekoster@gmail.com>"

WORKDIR /app/

COPY ./backend/requirements.txt /tmp/requirements.txt
COPY ./backend/dev-requirements.txt /tmp/dev-requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r /tmp/dev-requirements.txt ; fi"

ENV PYTHONPATH=/app/backend

COPY ./backend/scripts /app/backend/scripts

COPY ./backend/alembic.ini /app/backend
COPY ./backend/app /app/backend/app

WORKDIR /app/backend/

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
