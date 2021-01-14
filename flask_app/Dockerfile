FROM ubuntu:latest

USER root 

RUN apt-get update  && apt-get upgrade -y && apt-get clean

RUN apt-get install python3 -y

RUN apt update && DEBIAN_FRONTEND=noninteractive \
    apt install -y --no-install-recommends \
    python3-dev python3-pip python3-venv \
    libenchant1c2a

RUN pip3 install --upgrade pip

RUN apt-get install libenchant1c2a -y 

SHELL ["/bin/bash", "-c"]

RUN python3 -m venv env

RUN source env/bin/activate

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt


EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:$PORT  wsgi:app
# CMD gunicorn --bind 0.0.0.0:$PORT wsgi