FROM python:3.8
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN apt-get update \
    && apt-get clean \
    && apt-get update -qqq \
    && apt-get install -y -q build-essential graphviz graphviz-dev \
    && pip install --upgrade pip \
    && pip install Cython scipy \
    && pip install -r requirements.txt

RUN ipython profile create
COPY ./start.ipy /root/.ipython/profile_default/startup/

VOLUME /notebooks
WORKDIR /notebooks

# Run shell command for notebook on start
CMD jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root
