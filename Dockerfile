FROM python:3.7.1-alpine3.8
MAINTAINER webmaster@gjk.cz

ENV PYTHONBUFFERED 1

RUN mkdir /src
WORKDIR /src

ADD requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt
RUN apk add nodejs npm

ADD . /src

RUN cd /src/frontend; npm install
RUN npm install webpack
RUN cd /src/frontend; /src/frontend/node_modules/.bin/webpack
RUN cd /

RUN python /src/manage.py makemigrations
RUN python /src/manage.py migrate

CMD ["python", "/src/manage.py" , "runserver", "0.0.0.0:80"]
EXPOSE 80
