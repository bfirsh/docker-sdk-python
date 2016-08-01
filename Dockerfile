FROM python:2.7

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY test-requirements.txt /code/test-requirements.txt
RUN pip install -r test-requirements.txt

COPY . /code
RUN pip install .
