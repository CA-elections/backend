FROM python:stretch
MAINTAINER volby@gjk.cz

ENV PYTHONBUFFERED 1

RUN mkdir /src
WORKDIR /src


RUN apt-get update && apt-get install -y apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get -y update
RUN env ACCEPT_EULA=Y apt-get -y install unixodbc-dev msodbcsql17
ADD requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get -y install -y nodejs npm

ADD . /src

RUN odbcinst -i -s -f /src/db.ini -l
RUN cd /src/frontend; npm install
RUN npm install webpack
RUN cd /src/frontend; /src/frontend/node_modules/.bin/webpack --define process.env.URL="'volby.gjk.cz'" || true
RUN cd /
RUN ln -s /src/frontend/dist /src/frontend/static/dist
RUN ln -s /src/frontend/node_modules /src/frontend/static/node_modules

RUN python /src/manage.py makemigrations
RUN python /src/manage.py makemigrations api
RUN python /src/manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('user', 'volby@gjk.cz', 'test')" | python manage.py shell; exit 0
RUN python /src/manage.py collectstatic
RUN cd /src; nohup ./setupdaemon.py > daemonlog &

WORKDIR "/src"
CMD ["./start.sh"]
EXPOSE 80
