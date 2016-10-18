FROM python:latest
RUN pip install scrapy pandas
WORKDIR /usr/src/beveridge
COPY src .
CMD bash