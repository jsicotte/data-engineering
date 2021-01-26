FROM master-image:latest
RUN yum -y groupinstall 'Development Tools'

ENV PATH="/hadoop-2.7.6/bin:${PATH}"

COPY requirements.txt /

RUN pip3 install venv-pack
RUN python3 -m venv venv venv
RUN source venv/bin/activate ; pip install --upgrade pip
RUN source venv/bin/activate ; pip install -r requirements.txt
RUN venv-pack -p /venv
#will create venv.tar.gz