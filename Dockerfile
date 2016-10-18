FROM python:latest
RUN pip install scrapy pandas sklearn
RUN pip install scipy
WORKDIR /usr/src/beveridge
COPY src .
CMD bash