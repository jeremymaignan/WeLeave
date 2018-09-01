#!/bin/bash

cron
export FLASK_APP='routing.py'
cd src && flask run --host=0.0.0.0