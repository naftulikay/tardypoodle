FROM python:2.7.12
MAINTAINER Naftuli Kay <me@naftuli.wtf>

RUN mkdir -p /app
WORKDIR /app
ADD src /app/src
COPY bootstrap.py buildout.cfg setup.py requirements.txt /app/

RUN python bootstrap.py
RUN bin/buildout
RUN bin/test

ENTRYPOINT ["/app/bin/tardypoodle"]
