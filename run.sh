#!/bin/bash
echo 'Kill all Chrome and Chromedriver processes...'
pkill -f chrome
pkill -f chromedriver
echo 'Starting SH file...'
date
cd /home/alex/Price-monitoring-project/Prices-Parser/ && \
source /home/alex/Price-monitoring-project/Prices-Parser/venv.sh && \
/home/alex/Price-monitoring-project/venv/bin/python \
/home/alex/Price-monitoring-project/Prices-Parser/main.py >> /home/alex/Price-monitoring-project/Prices-Parser/parsing_lerua.log 2>&1