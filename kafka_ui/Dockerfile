FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app/

RUN pip install poetry 

RUN poetry config virtualenvs.create false

RUN poetry install

CMD [ "poetry","run","uvicorn","kafka.main:app","--host","0.0.0.0","--reload" ]