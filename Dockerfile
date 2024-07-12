FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY ./media_service /app/media_service
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]