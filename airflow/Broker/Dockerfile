FROM ubuntu:18.04

ENV mysql_config_path /etc/mysql/
ENV LANG C.UTF-8
ENV TZ Europe/Minsk
ENV DEBIAN_FRONTEND noninteractive
RUN ["apt-get", "update"]
RUN ["apt-get","install","-y", "python-minimal", "python-pip"]
RUN ["apt-get", "install", "-y", "default-libmysqlclient-dev"]
RUN ["pip", "install", "apache-airflow[celery,mysql]", "crypto"]
RUN ["pip", "install", "--force-reinstall", "Werkzeug==0.15.0"]
ADD airflow.cfg /root/airflow/

RUN ["pip", "install", "celery[redis]"]
ADD celeryconfig.py /usr/lib/python2.7/
