FROM python:3.12-bullseye

RUN apt-get update

RUN wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add -
RUN echo 'deb https://debian.neo4j.com stable latest' | tee -a /etc/apt/sources.list.d/neo4j.list
RUN apt-get update

RUN echo "neo4j-enterprise neo4j/accept-license select Accept evaluation license" | debconf-set-selections
RUN apt-get -y install neo4j-enterprise=1:5.15.0

EXPOSE 7474 7473 7687

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

ENV PORT=3000 SCHEME="bolt" ADDRESS='localhost:7687'

EXPOSE 3000

RUN chmod +x ./start.sh

CMD [ "./start.sh" ]