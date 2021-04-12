#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os, platform
import glob
import zipfile
import chardet
import requests
from ..utils import logging


def get_folder_root():
    folder_ = ''
    try:
        folder_ = os.environ['BR_OUT_FOLDER']
    except Exception as e:
        pass

    logging.debug('Getting csv folder root: \'{}\''.format(folder_))
    return folder_


def get_real_path():
    return os.getcwd()+'\\' if (platform.system() == 'Windows') else os.getcwd()+'/'


class ManageFileUtil:

    @staticmethod
    def get_file_encoding(filename):
        with open(filename, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']
        return encoding

    @staticmethod
    def get_folder_in():
        return get_folder_root()

    @staticmethod
    def get_folder_out():
        return get_folder_root()

    @staticmethod
    def data_frame_to_csv(filename, data_frame, encoding='utf-8'):
        data_frame.to_csv(filename, encoding=encoding, sep=';', index=False)
        logging.info('ManageFileUtil CSV file {} created with {} lines'.format(filename, len(data_frame)))

    @staticmethod
    def rename_file(source, target):
        """
            Rename the file source with the target name.

            :param source:
            :param target:

            :return
                File with the new name:
        """
        try:
            os.rename(source, target)
        except Exception as e:
            logging.error('File Error! {}'.format(e))

    @staticmethod
    def download_file(url, name):
        """
            Download the content of url in the file name parameter
        :param url:
        :param name:
        :return:
            None
        """
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
        logging.info('File downloaded in: {}'.format(name))

    @staticmethod
    def unzip_file(source_file, target_path):
        with zipfile.ZipFile(source_file, "r") as zip_ref:
            zip_ref.extractall(target_path)

    @staticmethod
    def delete_file(file):
        try:
            for f in glob.glob(file):
                os.remove(f)
        except OSError as e:
            logging.error('File Error! {}'.format(e))

    @staticmethod
    def file_exists(file):
        try:
            f = open(file)
            f.close()
            return True
        except IOError as e:
            logging.error('File Error! {}'.format(e))
            return False

    @staticmethod
    def get_list_of_files(regex):
        return glob.glob(regex)
