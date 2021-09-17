FROM debian:latest
FROM python:3.9.7-slim-buster

WORKDIR /detector

# Installing Requirements
RUN pip3 install -U pip
COPY requirements.txt .
RUN apt-get update && upgrade -y
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copying All Source
COPY . .

# Starting Bot
CMD ["python3.9", "detector.py"]