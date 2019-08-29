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

RUN yum install -y gcc openssl-devel bzip2-devel libffi libffi-devel
RUN yum install -y make
RUN yum install -y wget
RUN wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
RUN tar xzf Python-3.7.0.tgz
RUN cd cd Python-3.7.0; \
    Python-3.7.0/configure --enable-optimizations
RUN cd cd Python-3.7.0; \
    make altinstall

RUN yum install -y which
#RUN ln -fs /usr/local/bin/python3.7 /usr/bin/python
