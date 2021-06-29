FROM python:3.9-alpine

MAINTAINER Jonathan Kelley <jonk@uberleet.org>

ADD . /app/

WORKDIR /app

RUN python3 setup.py install

ENTRYPOINT ["fetch_rewards_assessment"]
