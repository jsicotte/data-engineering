FROM centos:6

RUN yum install -y java-1.8.0-openjdk-devel 
RUN yum install -y openssh-server openssh-clients
ADD hadoop-2.7.6.tar.gz /
COPY core-site.xml /hadoop-2.7.6/etc/hadoop/
COPY hdfs-site.xml /hadoop-2.7.6/etc/hadoop/
COPY mapred-site.xml /hadoop-2.7.6/etc/hadoop/
COPY slaves /hadoop-2.7.6/etc/hadoop/
COPY yarn-site.xml /hadoop-2.7.6/etc/hadoop/
COPY custom-start.sh /
RUN mkdir /hadoop-2.7.6/logs