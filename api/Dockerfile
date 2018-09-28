FROM python:3.7

# API
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=0
COPY . /var/app/api/
WORKDIR /var/app/api/
EXPOSE 5000
WORKDIR /var/app/api/
RUN pip3.7 -q install -r requirements.txt

# CRON
RUN apt-get -qq update
RUN apt-get -qq -y upgrade
RUN apt-get -qq install -y cron
RUN crontab engine.cron

ENTRYPOINT ["bash", "-c"]
CMD ["/var/app/api/entrypoint.sh"]