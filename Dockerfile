FROM continuumio/anaconda3:2021.05

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN conda install -c schrodinger pymol=2.4
RUN conda install biopython=1.78
RUN pip install --upgrade networkx==2.8.1
RUN pip install --upgrade scipy==1.8.1

RUN useradd -ms /bin/bash submitter
USER submitter

ADD src /home/submitter/src
WORKDIR /home/submitter/src
