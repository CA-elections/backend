FROM python:3
MAINTAINER jan.ruzicka01@gmail.com

RUN pip install --no-cache-dir requirements.txt

CMD ["python", "./something.py"]
