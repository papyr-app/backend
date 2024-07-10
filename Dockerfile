FROM python:3.11

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod u+x ./scripts/entrypoint.sh
ENTRYPOINT ["./scripts/entrypoint.sh"]
