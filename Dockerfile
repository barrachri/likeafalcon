FROM python:3.6.3

LABEL maintainer "barrachri@gmail.com"

USER root

RUN mkdir /src
WORKDIR /src
COPY requirements /src/requirements

# Install python packages
RUN pip install protobuf
RUN pip --no-cache-dir install -r requirements/common.txt

COPY . /src

CMD ["python", "main.py", "0.0.0.0"]