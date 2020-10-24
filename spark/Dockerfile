FROM java:8-jdk-alpine

RUN apk add --no-cache bash
RUN apk --no-cache add procps
RUN apk --update add coreutils
ADD spark-2.4.0-bin-hadoop2.7.tgz /
COPY spark-defaults.conf /spark-2.4.0-bin-hadoop2.7/conf/
RUN apk add iputils
