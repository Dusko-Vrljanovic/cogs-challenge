FROM ubuntu:22.04

EXPOSE 8000

WORKDIR /app
COPY requirements.txt /app
COPY .env.docker /app/.env

RUN apt update
RUN apt upgrade -y
RUN apt install -y python-is-python3 python3-pip
RUN apt autoremove -y
RUN apt clean -y
RUN pip install -r requirements.txt