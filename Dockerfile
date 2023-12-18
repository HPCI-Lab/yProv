FROM python:3-alpine

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

ENV PORT=3000 ADDRESS='db:7687'

EXPOSE 3000

CMD [ "python" , "./app.py" ]