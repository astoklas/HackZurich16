FROM python:2.7-slim
MAINTAINER Alexander Stoklasa <astoklas@cisco.com>
WORKDIR /usr/src
ADD ./requirements.txt /usr/src/
ADD ./vendingMachine.py /usr/src/

RUN pip install -r /usr/src/requirements.txt

CMD ["/usr/local/bin/python2.7" "/usr/src/vendingMachine.py"]
