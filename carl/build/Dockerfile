FROM python:3.11-bullseye

WORKDIR /python-docker
COPY requirements.txt requirements.txt
COPY frontend/ /python-docker/
RUN pip3 install -r requirements.txt

CMD [ "waitress-serve", "app:app" ]

