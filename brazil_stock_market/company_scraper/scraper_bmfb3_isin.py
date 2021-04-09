#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from ..utils import logging
import tqdm
import base64
import re
import json
import requests
import urllib3
from ..utils.array_utils import split_array
from ..utils.manage_threads import create_threads
from ..utils.pandas_util import PandasUtil
from ..utils.constants import (
    B3_SISWEBB3_BASE,
    B3_SISWEBB3_FILTER_LEGAL_ID,
    B3_SISWEBB3_ISINPAGE
)


urllib3.disable_warnings()
NUM_CIA_THREADS = 10


def encode_b64(text):
    id_base64 = text.encode('ascii')
    base64_bytes = base64.b64encode(id_base64)
    return base64_bytes.decode('ascii')


class CompanyScraper:

    stock_df = PandasUtil.new_data_frame(data=None)

    @staticmethod
    def fill_stock_information(origin_df):
        """
            Start of company Stock model information scraper. This flow use threads to improve performance.
            Based on list of CIAs legal_id search for complementary information in stock exchange portal.
        :param origin_df: (list of legal_id)
        :return: df_stock
        """
        logging.info("fill_stock_information")
        split_df, pbar_size = split_array(NUM_CIA_THREADS, origin_df), range(len(origin_df))
        with tqdm.tqdm(pbar_size) as pbar:
            threads = CompanyScraper.update_cia_stock(pbar, split_df, CompanyScraper.update_cia_from_reports)
            # manager join threads
            for t in threads:
                t.join()

        return CompanyScraper.stock_df

    @staticmethod
    def update_cia_stock(pbar, list_of_df, method_exec):
        threads = []
        pbar.set_description("Processing Companies "+method_exec.__name__)
        for index, arr in enumerate(list_of_df):
            threads.append(create_threads(str('T' + str(index) + '_' + method_exec.__name__),
                                                [arr, pbar],
                                                method_exec))
        for t in threads:
            t.start()
        logging.info('{} threads created! -> \n{}'.format(len(threads), [t.name for t in threads]))
        return threads

    @staticmethod
    def update_cia_from_reports(cias_cad_df, pbar):
        logging.debug("update_cia_from_reports")

        stock_t = {'LEGAL_ID': [], 'ISIN': [], 'TICKER': [], 'TYPE': [], 'CFI_COD': [], 'CURRENCY': []}

        for index, row in cias_cad_df.iterrows():
            df_report = CompanyScraper.search_by_legal_id(row['LEGAL_ID'])
            df_report = CompanyScraper.filter_(df_report, row['FINANCE_CATEGORY'])
            if not df_report.empty:
                for index2, row2 in df_report.iterrows():
                    stock_t['LEGAL_ID'].append(row['LEGAL_ID'])
                    stock_t['ISIN'].append(row2['isin'])
                    stock_t['TICKER'].append(CompanyScraper.generate_ticker_from_isin(row2['isin']))
                    stock_t['TYPE'].append(row2['isin'][6:9])
                    stock_t['CFI_COD'].append(row2['cfi'])
                    stock_t['CURRENCY'].append(row2['moeda'])

            pbar.update(1)
        # TODO- VERIFY CONCURRENCY DURING ACCESS AND WRITE BY THE THREADS
        CompanyScraper.stock_df = CompanyScraper.stock_df.append(PandasUtil.new_data_frame(stock_t), sort=True)
        CompanyScraper.stock_df = CompanyScraper.stock_df.loc[CompanyScraper.stock_df['TICKER'] != '']
        logging.debug('update_cia_from_reports -> {}'.format(CompanyScraper.stock_df))

    @staticmethod
    def generate_ticker_from_isin(isin) -> str:
        """
            Extract information from ISIN (ISO 6166) based on the formatter and Code documentation from stock exchange.

            ISIN formatter definition  [BR - AAAA - BBB - CC - D]
            BR / Brazil fixed
            AAAA / Emitter company code
            BBB / Type of asset
            CC / Complementary type information
            D / Control digit

            BBB -> CTF == Cote of funds
            BBB -> ACM == Nominative stocks
            BBB -> CDA == Units
        :param isin:
        :return:
        """
        # TODO Improve to remove the constant from code and create a filter that can be generic and extendible.
        ticker = ''
        if isin:
            emitter_code = isin[2:6]
            type_ = isin[6:9]
            category = isin[9:11]
            if type_ == 'CTF':
                ticker = emitter_code + '11'

            if type_ == 'ACN':
                if category == 'OR':
                    ticker = emitter_code + '3'
                elif category == 'PR':
                    ticker = emitter_code + '4'

            if type_ == 'CDA':
                ticker = emitter_code + '11'

        return ticker

    @staticmethod
    def search_by_legal_id(legal_id):
        """
            Based on legal_id search in B3 from ISIN registered.
        :param legal_id:
        :return:
        """
        logging.debug('search_by_legal_id: {}'.format(legal_id))

        # convert to base64 the legal_id to search
        token = encode_b64(json.dumps({'identifier': re.sub('[^A-Za-z0-9]+', '', legal_id)}))

        # search by legal_id and identify the legacy_system identification
        url = str(B3_SISWEBB3_BASE + B3_SISWEBB3_FILTER_LEGAL_ID).format(token)
        response = requests.get(url, verify=False).json()
        df_result = PandasUtil.new_data_frame(response['results'])

        if not df_result.empty:
            # get relevant information, id and cod_base
            id_legacy = str(df_result['id'][0])
            token = encode_b64(json.dumps({'code': id_legacy}))

            # search for list of isin related to the company and create stock model
            url = str(B3_SISWEBB3_BASE + B3_SISWEBB3_ISINPAGE).format(token)
            response = requests.get(url, verify=False).json()
            return PandasUtil.new_data_frame(response['results'])

        return PandasUtil.new_data_frame(data=None)

    @staticmethod
    def filter_(df_report, finance_category):
        """
            Filter data frame to remove stock that can't be used or isn't important.
            CFI Classification of Financial Instruments (ISO 10962) formatter definition [@ # $$$$]
            @ / CFI Category
            # / CFI Group
            $$$$ / Group attributes

                REIT's
                C - COLLECTIVE INVESTMENT VEHICLES
                I – STANDARD (VANILLA)INVESTMENT FUNDS/MUTUAL FUNDS

                Stock companies
                E - EQUITY

        :param df_report:
        :param finance_category:
        :return: df_report: (filtered)
        """
        if not df_report.empty:
            # For REITs filter only CFI starts with 'CI'
            '''
                CFI (ISO 10962)
                C - COLLECTIVE INVESTMENT VEHICLES
                I – STANDARD (VANILLA)INVESTMENT FUNDS/MUTUAL FUNDS
            '''
            if finance_category == 'FII':
                df_report = df_report.loc[df_report['cfi'].str.startswith('CI', na=False)]

            # For CIAs filter only CFI starts with 'E'
            ''' 
                CFI (ISO 10962)
                E - EQUITY
            '''
            if finance_category == 'CIA':
                df_report = df_report.loc[df_report['cfi'].str.startswith('E', na=False)]
                # ACN Nominal stock CDA Units
                df_report = df_report.loc[df_report['isin'].str.contains('ACN|CDA')]

        return df_report
