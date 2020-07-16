FROM python:3.5.9-buster

RUN pip3 install --upgrade pip
RUN pip3 install mlflow==1.8.0
RUN pip3 install mysql-connector-python
RUN pip3 install boto3
RUN apt-get update
RUN apt-get install python-mysqldb
RUN pip3 install mysqlclient
RUN pip3 install pymysql