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
RUN cd /src/frontend; /src/frontend/node_modules/.bin/webpack --define process.env.URL="'localhost:8000'" || true
RUN cd /
RUN mv /src/frontend/dist /src/frontend/static/dist
RUN mv /src/frontend/node_modules /src/frontend/static/node_modules

RUN python /src/manage.py makemigrations
RUN python /src/manage.py makemigrations api
RUN python /src/manage.py migrate
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('user', 'webmaster@gjk.cz', 'user')" | python manage.py shell
RUN python /src/manage.py collectstatic

CMD ["python", "/src/manage.py" , "runserver", "0.0.0.0:80"]
EXPOSE 80
