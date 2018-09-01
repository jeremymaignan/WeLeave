FROM python:3.7

# API
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=0
COPY . /var/app/api/
WORKDIR /var/app/api/
EXPOSE 5000
WORKDIR /var/app/api/
RUN pip3.7 install -r requirements.txt

# CRON
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y cron
RUN crontab engine.cron
RUN cron

ENTRYPOINT ["bash", "-c"]
CMD ["/var/app/api/entrypoint.sh"]