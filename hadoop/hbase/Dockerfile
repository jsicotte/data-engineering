FROM centos:6

RUN yum install -y java-1.8.0-openjdk-devel
RUN yum install -y iputils 
ADD hbase-2.3.1-bin.tar.gz /
ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.212.b04-0.el6_10.x86_64/jre
COPY hbase-site.xml /hbase-2.3.1/conf/
COPY regionservers /hbase-2.3.1/conf/