#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from ..utils import logging
from datetime import date, datetime, timedelta

from ..utils.download_files_util import DownloadFilesUtil
from ..company_scraper.market_data_information import MarketDataManager


class MarketDataScraper:
    """
        Class responsible to scraper basic information, changes in the number of reit's or cia's. Here
        only registry information is updated, new companies or companies that are not available anymore.
    """
    def __init__(self):
        print("Market Data")

    @staticmethod
    def scraper_market_information():
        """
            Scraper basic information, for the number of changes once a weekend or month it's enough.
        :return:
        """
        logging.info('##############################################################################')
        logging.info('# Start the process to find the registries and create a local data structure.#')
        logging.info('##############################################################################')

        try:
            # Download list of company listed on market
            DownloadFilesUtil.download_files_registration()

            # Include company information in the data model
            MarketDataManager.normalize_data_from_files()

            # Complete information
            MarketDataScraper.__scraper_stock_information__()
            logging.info("### Process ended ###")
        except Exception as e:
            logging.error("======> {}".format(e))

    @staticmethod
    def __scraper_stock_information__():
        logging.info("scraper_stock_information")
        # Scraper information of company stock
        MarketDataManager.fill_company_stock_information()

    @staticmethod
    def update_series_data():
        """
            To keep updated the base of assets, now only daily.
        :return:
        """
        logging.info('###########################################################')
        logging.info('# Update the base of assets with the recent historic data.#')
        logging.info('###########################################################')
        try:
            # identify last update and download necessary files
            last_date = MarketDataManager.get_last_series_update()
            if not last_date:
                # download series for the current year
                file_name = date.today().year
                DownloadFilesUtil.stock_market_series(file_name='A'+str(file_name))

            else:
                # create a list of days to download
                today = datetime.today()
                delta = (today - last_date).days
                date_list = [(last_date + timedelta(days=x)).strftime('%d%m%Y') for x in range(1, delta+1)]

                # iterate this list doing the download
                for item in date_list:
                    DownloadFilesUtil.stock_market_series(file_name='D'+item)

            # process files
            MarketDataManager.fill_stock_historic_data()
            logging.info("### Update ended ###")
        except Exception as e:
            logging.error("======> {}".format(e))

