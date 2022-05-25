FROM python:3.9
MAINTAINER 'https://github.com/deficoder'

COPY . /code

WORKDIR /code/app

RUN pip install --upgrade pip && pip install -r ../requirement.txt

EXPOSE 80