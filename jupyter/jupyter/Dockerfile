FROM jupyter/all-spark-notebook

RUN conda remove pyzmq
RUN conda install pyzmq=14.6.0
RUN pip install "ipython[notebook]"
ADD hadoop-2.7.6.tar.gz /
RUN mkdir /opt/conda/share/jupyter/kernels/pyspark
COPY kernel.json /opt/conda/share/jupyter/kernels/pyspark