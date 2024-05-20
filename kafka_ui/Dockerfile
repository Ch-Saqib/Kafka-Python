FROM python:3.12

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

    
WORKDIR /app

COPY . /app/

RUN pip install poetry 

RUN poetry config virtualenvs.create false


RUN poetry install --no-interaction --no-root

CMD [ "poetry","run","uvicorn","kafka.main:app","--host","0.0.0.0","--reload" ]
