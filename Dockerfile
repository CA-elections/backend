FROM python:3
MAINTAINER jan.ruzicka01@gmail.com

ENV PYTHONBUFFERED 1

RUN mkdir /src
WORKDIR /src

ADD requirements.txt /src/
RUN pip install --no-cache-dir -r /src/requirements.txt

ADD . /src/

CMD ["python", "/src/Elections/manage.py", "runserver", "0.0.0.0:8000"]
