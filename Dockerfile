FROM debian:latest
FROM python:3.9.7-slim-buster

WORKDIR /detector

# Installing Requirements
RUN pip3 install -U pip
RUN apt-get update && apt-get upgrade -y
COPY requirements.txt .
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Copying All Source
COPY detector.py .

# Starting Bot
CMD ["python3.9", "detector.py"]
