FROM centos:6

RUN yum install -y java-1.8.0-openjdk-devel 
RUN yum install -y openssh-server openssh-clients

RUN yum install -y gcc openssl-devel bzip2-devel libffi libffi-devel
RUN yum install -y make
RUN yum install -y wget
RUN wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
RUN tar xzf Python-3.7.0.tgz
RUN cd cd Python-3.7.0; \
    Python-3.7.0/configure --enable-optimizations
RUN cd cd Python-3.7.0; \
    make altinstall

COPY apache-atlas-2.1.0 /apache-atlas-2.1.0

COPY hbase-site.xml /apache-atlas-2.1.0/conf/hbase
COPY atlas-application.properties /apache-atlas-2.1.0/conf
COPY atlas_config.py /apache-atlas-2.1.0/bin

WORKDIR /apache-atlas-2.1.0/server/webapp/
RUN /usr/lib/jvm/java-1.8.0-openjdk.x86_64/bin/jar -xf /apache-atlas-2.1.0/server/webapp/atlas.war