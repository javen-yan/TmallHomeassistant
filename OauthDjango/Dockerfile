FROM python:3.6.4
ENV HOME /app/oauth_django
COPY . $HOME
WORKDIR $HOME

RUN pip install --upgrade pip
RUN pip install peewee
RUN pip install click
RUN pip install Django
RUN pip install mysqlclient
RUN pip install requests

RUN pip install uwsgi
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

RUN chown 1002:1002 /app -R

USER 1002

CMD uwsgi --ini app.ini