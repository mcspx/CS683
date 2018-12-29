FROM python:3.7-alpine

ENV BIND_PORT 5000

ADD . /code

WORKDIR /code

EXPOSE 80/tcp
EXPOSE 443/tcp
EXPOSE $BIND_PORT

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
