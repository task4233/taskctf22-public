FROM ubuntu:20.04

ENV NAME ANTI_DETECTION_APP

RUN mkdir /var/www
WORKDIR /var/www

RUN apt-get update \
 && apt-get install -y \
  build-essential \
  libfuzzy-dev \
  libfuzzy2 \
  python3 \
  python3-pip

COPY . .

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
RUN chmod 755 -R /var/www
RUN adduser -u 1000 anti-detection
USER anti-detection

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]
