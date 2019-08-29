FROM centos:7

RUN yum install -y java-1.8.0-openjdk-devel
RUN yum -y update
RUN yum install -y curl
RUN yum install -y gcc openssl-devel bzip2-devel libffi libffi-devel
RUN yum install -y make
RUN yum install -y wget
RUN yum install -y epel-release
RUN yum update
RUN yum list | grep sqlite
RUN yum install -y libsqlite3x-devel
RUN wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
RUN tar xzf Python-3.7.0.tgz
RUN cd cd Python-3.7.0; \
    Python-3.7.0/configure --enable-optimizations
RUN cd cd Python-3.7.0; \
    make altinstall
RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py
RUN python3.7 get-pip.py
#RUN pip3 install pyspark
RUN pip3 install --upgrade pip
RUN pip3 install jupyter