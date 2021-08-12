FROM python:3.6-alpine

MAINTAINER Ethan Maintainers "42188007@qq.com"

WORKDIR /opt/zero_cloud

COPY requirement.txt /opt/zero_clod/requirement.txt

COPY app.py /opt/zero_cloud/app.py

COPY config_files /opt/zero_cloud/config_files

COPY controller /opt/zero_colud/controller

COPY utils /opt/zero_clould/utils

RUN pip3 install -i https://pypi.douban.com/simple  -r /requirement.txt

CMD ["python3", "app.py"]
