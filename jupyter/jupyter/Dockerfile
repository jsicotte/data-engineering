FROM dask_submit-test:latest
RUN yum install -y python3-devel
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN pip3 install dask-labextension
RUN pip3 install jupyterlab
RUN jupyter serverextension enable --sys-prefix jupyter_server_proxy
COPY jupyter_lab_config.py /root/.jupyter/
COPY config.yaml /etc/dask/
#RUN conda remove pyzmq
#RUN conda install pyzmq=14.6.0
#RUN pip install "ipython[notebook]"
#ADD hadoop-2.7.6.tar.gz /
#RUN mkdir /opt/conda/share/jupyter/kernels/pyspark
#COPY kernel.json /opt/conda/share/jupyter/kernels/pyspark