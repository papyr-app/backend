FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/scripts/entrypoint.sh

RUN ls -l /app/scripts

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
