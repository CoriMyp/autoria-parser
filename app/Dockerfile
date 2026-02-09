FROM python:3.14.0

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN ["python", "app/main.py"]
