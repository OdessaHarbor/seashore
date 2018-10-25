FROM python:3.7.0-alpine

ENV INSTALL_PATH /Converter_api
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 127.0.0.1:8000 --access-logfile - "Converter_api.app:create_converter()"
 