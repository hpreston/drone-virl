# Docker image for a Drone plugin for Cisco VIRL
FROM python:3.6-alpine3.6
MAINTAINER Hank Preston <hank.preston@gmail.com>

RUN mkdir -p /bin/drone-plugin
WORKDIR /bin/drone-plugin

COPY requirements.txt /bin/drone-plugin/
RUN pip install -r requirements.txt

ADD samples /bin/drone-plugin/samples

ADD droneci /bin/drone-plugin/droneci

COPY virlutils.py /bin/drone-plugin/
COPY drone_virl.py /bin/drone-plugin/

ENTRYPOINT ["python", "/bin/drone-plugin/drone_virl.py"]
