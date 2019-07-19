#!/usr/bin/env bash

if [ ! -f "/formatted" ]
then
    /hadoop-2.7.6/bin/hdfs namenode -format
    touch /formatted
fi

/hadoop-2.7.6/bin/hdfs namenode