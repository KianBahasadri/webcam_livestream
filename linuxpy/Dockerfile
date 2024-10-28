FROM python:3.12-alpine
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

COPY main.py main.py
COPY index.html index.html

RUN apk add openssl
RUN openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"


ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--reload", "--ssl-keyfile=./key.pem", "--ssl-certfile=./cert.pem"]

