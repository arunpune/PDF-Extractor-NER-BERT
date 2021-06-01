FROM python:3.8

MAINTAINER Atharva Bankar <bankaratharva@gmail.com>

CMD ["echo", "PDF Extraction Tool"]

RUN apt-get update
RUN apt-get install poppler-utils -y
RUN apt-get -y install tesseract-ocr

ADD requirements.txt /
RUN pip install -r /requirements.txt

ADD . /app
WORKDIR /app

EXPOSE 5000
CMD [ "python" , "app.py"]