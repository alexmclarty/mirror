FROM python:3

WORKDIR /usr/src/app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv && pipenv install

COPY . .
EXPOSE 6001

CMD [ "pipenv", "run", "python", "app.py" ]
