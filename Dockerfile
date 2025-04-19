FROM python:3.11-slim

WORKDIR /app

COPY smartd_exporter.py .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]