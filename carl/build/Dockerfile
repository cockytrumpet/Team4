FROM python:3.11-bullseye

WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY frontend/ /python-docker/
CMD [ "waitress-serve", "app:app" ]

