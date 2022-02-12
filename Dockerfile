FROM python:3.9 as app

ENV WORKDIR=/app
WORKDIR $WORKDIR

COPY . $WORKDIR/
RUN pip install -r $WORKDIR/requirements.txt

RUN apt-get update \
    && apt-get install libyajl-dev -y \
    && apt-get install python3-dev -y

