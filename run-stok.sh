#!/bin/bash
echo 'Starting SH file - Parsing stok-centr.com site...'
date
cd /home/alex/Price-monitoring-project/Prices-Parser/ && \
source /home/alex/Price-monitoring-project/Prices-Parser/venv.sh && \
/home/alex/Price-monitoring-project/venv/bin/python \
/home/alex/Price-monitoring-project/Prices-Parser/main-stok.py >> /home/alex/Price-monitoring-project/Prices-Parser/ParserStockCentrWithSession.log 2>&1