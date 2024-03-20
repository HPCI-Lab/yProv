FROM python:3-alpine

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT=3000 SCHEME="bolt" ADDRESS='localhost:7687'

EXPOSE 3000

CMD [ "python" , "./app.py" ]