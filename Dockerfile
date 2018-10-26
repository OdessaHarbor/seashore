FROM python:3.7.0-alpine

ENV INSTALL_PATH /Converter
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:5000 --access-logfile - "Converter.app:create_converter()"
 