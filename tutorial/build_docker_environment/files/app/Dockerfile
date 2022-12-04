FROM ubuntu:20.04

RUN mkdir /var/www
WORKDIR /var/www

RUN apt-get update \
 && apt-get install -y \
  python3 \
  python3-pip

COPY . .

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
RUN chmod 755 -R /var/www
RUN adduser -u 1000 build-docker
USER build-docker

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]
