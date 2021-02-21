FROM python:2.7.13

WORKDIR /site

ADD requirements.txt .
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com && mkdir /logs/

ADD . .

EXPOSE 8000

CMD bash start.sh
