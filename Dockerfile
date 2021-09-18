FROM python:3.6-alpine

MAINTAINER Ethan Maintainers "42188007@qq.com"

WORKDIR /opt/zero_cloud

COPY requirement.txt \ 
     app.py \
     config_files \
     controller  \
     utils /opt/zero_clould/

RUN pip3 install -i https://pypi.douban.com/simple  -r /opt/zero_cloud/requirement.txt

