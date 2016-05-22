FROM ubuntu:trusty

MAINTAINER Ngerll Joe<huqiao@chinatowercom.cn>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install nginx  sed python-pip python-dev uwsgi-plugin-python
RUN apt-get -y install python-mysqldb

copy app /var/www/app
RUN sudo pip install -r /var/www/app/requirements.txt
copy supervisord.conf /etc/supervisord.conf
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
copy nginx.conf /etc/nginx/nginx.conf

WORKDIR /var/www/app
RUN sudo service nginx start
RUN sudo supervisord -c /etc/supervisord.conf
RUN sudo supervisorctl -c /etc/supervisord.conf start all
RUN sudo supervisorctl -c /etc/supervisord.conf status

EXPOSE 80

