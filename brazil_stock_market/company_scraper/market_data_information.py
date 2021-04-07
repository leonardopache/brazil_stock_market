#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from ..utils import logging
from ..utils.manage_file_util import ManageFileUtil
from ..utils.pandas_util import PandasUtil
from ..utils.constants import CIA_OPENED_CSV_NAME, FI_OPENED_CSV_NAME, COMPANY_MODEL, STOCK_MODEL, SERIES_MODEL
from ..company_scraper.manager_reit_data import ManagerREIT
from ..company_scraper.manager_cia_data import ManagerCIA
from ..company_scraper.manager_series_data import ManagerSeries
from ..company_scraper.scraper_bmfb3_isin import CompanyScraper

import pandas as pd


class MarketDataManager:
    """
        Class responsible to data normalization from files.
    """
    @staticmethod
    def normalize_data_from_files():
        """
            As in Brazil the stock companies and REITs are keep their register in distinct organization it's necessary
            to create a translate from each file and normalize in a common structure.
        :return:
        """
        logging.info('normalize_data_from_files')
        # REITs verify if the file .csv is in the folder IN
        reit_csv_file = ''.join([ManageFileUtil.get_folder_in() + FI_OPENED_CSV_NAME])
        if ManageFileUtil.file_exists(reit_csv_file):
            reit_df = ManagerREIT.load_info_into_dataframe(reit_csv_file)
            # transform df to model and update DB
            MarketDataManager.__transform_to_model_company__(reit_df, type_asset='REIT')

        # CIAs verify if the file .csv is in the folder IN
        cia_csv_file = ''.join([ManageFileUtil.get_folder_in(), CIA_OPENED_CSV_NAME])
        if ManageFileUtil.file_exists(cia_csv_file):
            cia_df = ManagerCIA.load_info_into_dataframe(cia_csv_file)
            # transform df to model and update DB
            MarketDataManager.__transform_to_model_company__(cia_df, type_asset='CIA')

    @staticmethod
    def __transform_to_model_company__(df, type_asset=None):
        # todo initial solution save in output csv
        logging.info('__transform_to_model_company__')
        if type_asset == 'REIT':
            # call method responsible for translate columns of reit_df into data model
            ms = ModelService()

            for index, row in df.iterrows():
                # print(row)
                ms.company['LEGAL_ID'].append(row['CNPJ_FUNDO'])
                ms.company['DENOMINATION'].append(row['DENOM_SOCIAL'])
                ms.company['REGISTRY_DATE'].append(row['DT_REG'])
                ms.company['LOCAL_MARKET_COD'].append(row['CD_CVM'])
                ms.company['COUNTRY'].append('BRA')
                ms.company['STOCK_EXCHANGE'].append('B3')
                ms.company['LEGAL_STATUS'].append(row['SIT'])
                ms.company['CITY'].append('')
                ms.company['SECTOR'].append('')
                ms.company['SUB_SECTOR'].append('')
                ms.company['ACTIVITY'].append('')
                ms.company['NET_EQUITY'].append(
                    round(
                        float(
                            row['VL_PATRIM_LIQ'] if len(row['VL_PATRIM_LIQ']) > 0 else 0
                        ), 4)
                )
                ms.company['FINANCE_CATEGORY'].append(row['TP_FUNDO'])
            ms.update_company(PandasUtil.new_data_frame(ms.company))

        if type_asset == 'CIA':
            # call method responsible for translate columns of cia_df into data model
            ms = ModelService()

            for index, row in df.iterrows():
                # print(row)
                ms.company['LEGAL_ID'].append(row['CNPJ_CIA'])
                ms.company['DENOMINATION'].append(row['DENOM_SOCIAL'])
                ms.company['REGISTRY_DATE'].append(row['DT_REG'])
                ms.company['LOCAL_MARKET_COD'].append(row['CD_CVM'])
                ms.company['COUNTRY'].append('BRA')
                ms.company['STOCK_EXCHANGE'].append('B3')
                ms.company['LEGAL_STATUS'].append(row['SIT_EMISSOR'])
                ms.company['CITY'].append(row['MUN'])
                ms.company['SECTOR'].append('')
                ms.company['SUB_SECTOR'].append('')
                ms.company['ACTIVITY'].append('')
                ms.company['NET_EQUITY'].append(float(0))
                ms.company['FINANCE_CATEGORY'].append('CIA')

            ms.update_company(PandasUtil.new_data_frame(ms.company))

    @staticmethod
    def fill_company_stock_information():
        """
            Scraper to fill information not present in the basic register .csv. In this step
            the scraper can be the officially stock exchange, 3rd party API or csv files.
        :return:
        """
        logging.info('fill_company_stock_information')
        ms = ModelService()
        # READ ROWS FROM COMPANY
        company_file = ''.join([ManageFileUtil.get_folder_out() + COMPANY_MODEL])
        if ManageFileUtil.file_exists(company_file):
            all_company_df = PandasUtil.read_file_csv(company_file)
            stock_df = CompanyScraper.fill_stock_information(all_company_df)
            ms.update_stock(stock_df)

    @staticmethod
    def fill_stock_historic_data():
        """
            If csv of historic series doesn't exists so load data from file.
        :return:
        """
        logging.info('fill_stock_historic_data')
        ms = ModelService()
        # list of txt files in folder
        txt_files_arr = ManageFileUtil.get_list_of_files(ManageFileUtil.get_folder_in()+'*.TXT')
        # for each file transform to series model
        for file in txt_files_arr:
            # transform df into series model
            series_df = ManagerSeries.load_info_into_dataframe(file)

            # update series csv file
            ms.update_series(series_df)
            ManageFileUtil.delete_file(file)

    @staticmethod
    def get_last_series_update():
        """
            Look into the series the last date updated
        :return:
        """
        logging.info('get_last_update')
        return ModelService().get_last_series_update()


class ModelService:
    company = {'LEGAL_ID': [],
                'DENOMINATION': [],
                'REGISTRY_DATE': [],
                'LOCAL_MARKET_COD': [],
                'COUNTRY': [],
                'STOCK_EXCHANGE': [],
                'LEGAL_STATUS': [],
                'CITY': [],
                'SECTOR': [],
                'SUB_SECTOR': [],
                'ACTIVITY': [],
                'NET_EQUITY': [],
                'FINANCE_CATEGORY': []
               }

    stock = {'LEGAL_ID': [],
             'ISIN': [],
             'TICKER': [],
             'TYPE': [],
             'CFI_COD': [],
             'CURRENCY': []
             }

    series = {'TICKER': [],
              'DATE': [],
              'OPEN': [],
              'HIGH': [],
              'LOW': [],
              'AVERAGE': [],
              'CLOSE': [],
              'NUM_TRADES': []}

    def update_company(self, df_):
        """
            Temporary solution using csv file, change to DB connection in future.
        :return:
        """
        logging.info('update_company')
        company_file = ManageFileUtil.get_folder_out() + COMPANY_MODEL
        if ManageFileUtil.file_exists(company_file):
            old_df = PandasUtil.read_file_csv(company_file)

            df_ = PandasUtil.merge(old_df, df_, how='right', on='LEGAL_ID', suffixes=('_old', ''))

        ManageFileUtil.data_frame_to_csv(company_file, df_)

    def update_stock(self, df_):
        """
            Temporary solution using csv file, change to DB connection in future.
        :param df_:
        :return:
        """
        logging.info('update_stock')
        stock_file = ManageFileUtil.get_folder_out() + STOCK_MODEL
        if ManageFileUtil.file_exists(stock_file):
            old_df = PandasUtil.read_file_csv(stock_file)

            df_ = PandasUtil.merge(old_df, df_, how='right', on='LEGAL_ID', suffixes=('_old', ''))

        ManageFileUtil.data_frame_to_csv(stock_file, df_)

    def update_series(self, df_):
        """
            Temporary solution using csv file, change to DB connection in future.
        :return:
        """
        logging.info('update_series')
        series_file = ManageFileUtil.get_folder_out() + SERIES_MODEL
        if ManageFileUtil.file_exists(series_file):
            old_df = PandasUtil.read_file_csv(series_file)
            df_ = old_df.append(df_)

        ManageFileUtil.data_frame_to_csv(series_file, df_)

    def get_last_series_update(self):
        """
            From series model find the date max
        :return:
        """
        series_csv_file = ''.join([ManageFileUtil.get_folder_out() + SERIES_MODEL])
        if ManageFileUtil.file_exists(series_csv_file):
            old_df = PandasUtil.read_file_csv(series_csv_file)
            old_df['DATE'] = pd.to_datetime(old_df['DATE'], dayfirst=True)
            return old_df['DATE'].max()
        else:
            return False
