#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from ..utils.constants import FI_CVM_CAD_URL, CIA_CVM_CAD_URL, BMF_SERIES_HIST, \
    CIA_OPENED_CSV_NAME, FI_OPENED_CSV_NAME
from ..utils import logging
from ..utils.pandas_util import PandasUtil
from ..utils.manage_file_util import ManageFileUtil


class DownloadFilesUtil:
    """
        Execute function to download updated information of FIIs and Companies.
    :return:
        None
    """

    @staticmethod
    def download_files_registration():
        logging.info('download_files_registration')
        DownloadFilesUtil.reit_register_information()
        DownloadFilesUtil.companies_register_information()

    @staticmethod
    def companies_register_information():
        """
            Companies information downloaded as 'files/in/inf_cadastral_cia_aberta.csv'
        :return:
        """
        try:
            file = ManageFileUtil.get_folder_in() + CIA_OPENED_CSV_NAME
            # CIA information
            data_frame = PandasUtil.read_html(CIA_CVM_CAD_URL, header=0)[0]
            last_cvs_file = data_frame['Name'][2]
            ManageFileUtil.delete_file(file)
            ManageFileUtil.download_file(CIA_CVM_CAD_URL + last_cvs_file, file)
        except Exception as err:
            logging.error('Error download CSV!! {}'.format(err))

    @staticmethod
    def stock_market_series(file_name):
        """
            B3 historic series
        :return:
        """
        try:
            file = ManageFileUtil.get_folder_in() + file_name
            ManageFileUtil.delete_file(file)
            ManageFileUtil.download_file(BMF_SERIES_HIST.format(file_name), file)
            ManageFileUtil.unzip_file(file, ManageFileUtil.get_folder_in())
            # delete zip file use the file_name
            ManageFileUtil.delete_file(file)
        except Exception as err:
            logging.error('Error download CSV!! {}'.format(err))

    @staticmethod
    def reit_register_information():
        """
            FII information downloaded as 'files/in/cad_fi.csv'
        :return:
        """
        try:
            file = ManageFileUtil.get_folder_in() + FI_OPENED_CSV_NAME
            ManageFileUtil.delete_file(file)
            ManageFileUtil.download_file(FI_CVM_CAD_URL + FI_OPENED_CSV_NAME, file)
        except Exception as err:
            logging.error('Error download CSV!! {}'.format(err))
