FROM python:3-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV PORT=3000 ADDRESS='host.docker.internal:7687' SCHEME='bolt' USER='neo4j' PASSWORD='password'

EXPOSE 3000

CMD [ "python" , "./app.py" ]