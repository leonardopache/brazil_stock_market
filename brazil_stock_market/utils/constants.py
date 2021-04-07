#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# list os constant links to consult values

CIA_OPENED_CSV_NAME = 'inf_cadastral_cia_aberta.csv'
FI_OPENED_CSV_NAME = 'cad_fi.csv'
COMPANY_MODEL = 'company.csv'
STOCK_MODEL = 'stock.csv'
SERIES_MODEL = 'series.csv'

CIA_CVM_CAD_URL = 'http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/'
FI_CVM_CAD_URL = 'http://dados.cvm.gov.br/dados/FI/CAD/DADOS/'

B3_SISWEBB3_BASE = 'https://sistemaswebb3-listados.b3.com.br/'
B3_SISWEBB3_FILTER_LEGAL_ID = 'isinProxy/IsinCall/GetListEmitterFilter/{}'
B3_SISWEBB3_ISINPAGE = 'isinProxy/IsinCall/GetEmitterCode/{}'

BMF_URL_BASE = 'http://bvmf.bmfbovespa.com.br/'
BMF_SERIES_HIST = BMF_URL_BASE + 'InstDados/SerHist/COTAHIST_{}.ZIP'
