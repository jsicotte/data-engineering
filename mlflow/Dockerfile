FROM python:3.8-buster

RUN pip3 install --upgrade pip
RUN pip3 install mlflow
RUN pip3 install mysql-connector-python
RUN pip3 install boto3
RUN apt-get update
RUN apt-get install python-mysqldb
RUN pip3 install mysqlclient
RUN pip3 install pymysql
RUN pip3 install PyMySQL[rsa]
COPY requirements.txt /
RUN pip3 install -r requirements.txt
