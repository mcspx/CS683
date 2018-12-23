FROM python:3.7-alpine
ADD . /code
WORKDIR /code
EXPOSE 80/tcp
EXPOSE 443/tcp
RUN pip install -r requirements.txt
CMD ["python", "app.py"]