FROM python:3
MAINTAINER jan.ruzicka01@gmail.com

ENV PYTHONBUFFERED 1

RUN mkdir /src
WORKDIR /src

ADD requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt

ADD . /src/

#RUN python /src/DockerTest/manage.py migrate

CMD ["python", "/src/DockerTest/manage.py" , "runserver"]
EXPOSE 8000:8000
