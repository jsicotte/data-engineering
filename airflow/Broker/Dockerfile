FROM ubuntu:18.04

ENV mysql_config_path /etc/mysql/
ENV LANG C.UTF-8
ENV TZ Europe/Minsk
ENV DEBIAN_FRONTEND noninteractive
RUN ["apt-get", "update"]
RUN ["apt-get","install","-y", "python3.6", "python3-pip"]
RUN ["apt-get", "install", "-y", "default-libmysqlclient-dev"]
RUN ["pip3", "install", "apache-airflow[celery,mysql]", "crypto"]
RUN ["pip3", "install", "--force-reinstall", "Werkzeug==0.15.0"]
ADD airflow.cfg /root/airflow/

RUN ["pip3", "install", "celery[redis]"]
ADD celeryconfig.py /usr/lib/python2.7/
