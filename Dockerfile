FROM python:3.9.6-slim as builder

WORKDIR /app

RUN apt-get update&& \
    apt-get install -y --no-install-recommends gcc&& \
    pip install --upgrade pip

RUN apt-get install -y git

RUN git clone https://github.com/benelungo/ScheduleBot.git /app
RUN pip install -r requirements.txt
