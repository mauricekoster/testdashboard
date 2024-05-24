FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

LABEL maintainer="Maurice Koster <mauricekoster@gmail.com>"

COPY requirements.txt /tmp/requirements.txt
COPY dev-requirements.txt /tmp/dev-requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r /tmp/dev-requirements.txt ; fi"


WORKDIR /app/

ENV PYTHONPATH=/app

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

COPY ./app /app/app

EXPOSE 80

CMD ["/start.sh", "prod"]
