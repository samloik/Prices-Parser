#!/bin/bash
echo 'Starting SH file...'
date
export ZABBIX_SERVER_ADDRESS='192.168.1.60'
echo 'ZABBIX_SERVER_ADDRESS='$ZABBIX_SERVER_ADDRESS
cd /home/alex/Price-monitoring-project/Prices-Parser/ && \
source /home/alex/Price-monitoring-project/Prices-Parser/venv.sh && \
/home/alex/Price-monitoring-project/venv/bin/python \
/home/alex/Price-monitoring-project/Prices-Parser/main.py >> /home/alex/Price-monitoring-project/Prices-Parser/parsing_lerua.log 2>&1