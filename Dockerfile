FROM ubuntu:trusty

MAINTAINER Ngerll Joe<huqiao@chinatowercom.cn>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install nginx  sed python-pip python-dev uwsgi-plugin-python
RUN apt-get -y install python-mysqldb

copy app /var/www/app
RUN sudo pip install -r /var/www/app/requirements.txt
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
copy nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

WORKDIR /var/www/app
RUN chmod 777 init.sh
RUN apt-get -y install ntpdate
ENTRYPOINT /var/www/app/init.sh
