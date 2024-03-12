#!/bin/bash
# Let's call this script venv.sh
source /home/alex/Price-monitoring-project/venv/bin/activate
export ZABBIX_SERVER_ADDRESS='192.168.1.60'
echo 'ZABBIX_SERVER_ADDRESS='$ZABBIX_SERVER_ADDRESS