FROM python:3.9-alpine

WORKDIR /app

ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY . .

RUN apk update \
    && for pkg in `cat packages.txt`;do apk add --no-cache $pkg;done

RUN pip install -r requirements.txt

CMD ["flask", "run"]
