FROM python:3
MAINTAINER Your Name "pamungkas.syahrizal@gmail.com"
RUN mkdir -p /demo
RUN mkdir -p /demo/storage/log
COPY . /demo
RUN pip install -r /demo/requirements.txt
WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]