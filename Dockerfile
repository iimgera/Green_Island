FROM python:3.11.3

ENV PYTHONUNBUFFERED 1 

RUN apt-get update && apt-get install -y \  
    postgresql-client 

RUN mkdir /app 

WORKDIR /app 

COPY requirements.txt /app/ 

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary


COPY . /app/