FROM ubuntu:18.04
RUN apt-get update
RUN apt-get -y install wget
RUN wget https://downloads.lightbend.com/scala/2.12.2/scala-2.12.2.deb
RUN apt install -y openjdk-8-jre-headless
RUN dpkg -i *.deb
ADD spark-2.4.4-bin-hadoop2.7.tgz /
COPY spark-defaults.conf /spark-2.4.4-bin-hadoop2.7/conf/