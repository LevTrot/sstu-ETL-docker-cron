FROM python:3.11

WORKDIR /app

COPY requirment.txt .
RUN pip install -r requirment.txt

COPY etl/ .

RUN apt-get update && apt-get install -y cron

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN touch /var/log/cron.log

CMD ["/entrypoint.sh"]

