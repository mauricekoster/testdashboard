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

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

WORKDIR /app/

ENV PYTHONPATH=/app



COPY ./scripts/ /app/
COPY ./alembic.ini /app/
COPY ./prestart.sh /app/
COPY ./tests-start.sh /app/

COPY ./app /app/app
EXPOSE 80

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]
