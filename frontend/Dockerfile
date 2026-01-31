FROM python:3.13

LABEL maintainer="Maurice Koster <mauricekoster@gmail.com>"

COPY ./frontend/requirements.txt /tmp/requirements.txt
COPY ./frontend/dev-requirements.txt /tmp/dev-requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then pip install -r /tmp/dev-requirements.txt ; fi"

WORKDIR /app/
COPY ./frontend/README.md /app/frontend/
COPY ./frontend/app /app/frontend/app

ENV PYTHONPATH=/app/frontend
WORKDIR /app/frontend/

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]


