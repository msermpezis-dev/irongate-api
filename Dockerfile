FROM python:3.10.13-alpine
WORKDIR /app

COPY requirements.txt .
COPY application/. .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./api.py" ]

EXPOSE 8080