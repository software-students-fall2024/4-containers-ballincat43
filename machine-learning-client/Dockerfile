FROM python:3.10

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install pipenv
RUN pipenv install --system --deploy

COPY . .

EXPOSE 1000

CMD ["python", "-m", "flask", "run", "--port=1000"]