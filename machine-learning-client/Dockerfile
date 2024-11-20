FROM python:3.10

WORKDIR /app

COPY . /app

RUN pipenv install

EXPOSE 101

CMD ["python", "functions.py"]