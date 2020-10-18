FROM centos:6

RUN yum install -y java-1.8.0-openjdk-devel
RUN yum install -y iputils 
RUN yum install -y wget
RUN wget https://archive.apache.org/dist/lucene/solr/8.6.3/solr-8.6.3.zip
RUN yum install -y unzip
RUN unzip solr-8.6.3.zip
RUN yum install -y lsof
COPY solr /atlas
CMD solr-8.6.3/bin/solr start -p 8984 -f