FROM python:3.10-slim

RUN mkdir /home/code

COPY requirements.txt /home/code

RUN apt-get update && apt-get -y install cron && cd /home/code && pip install -r requirements.txt

COPY . /home/code

COPY cron /etc/cron.d/cron
RUN chmod 0644 /etc/cron.d/cron && crontab /etc/cron.d/cron && touch /var/log/cron.log

WORKDIR /home/code
ENV PYTHONPATH="${PYTHONPATH}:/home/code/"
CMD ["./entry.sh"]