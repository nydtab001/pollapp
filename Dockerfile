FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY pollapp .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:3000"]
EXPOSE 3000/tcp
