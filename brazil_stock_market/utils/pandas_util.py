#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from ..utils import logging
from ..utils.manage_file_util import ManageFileUtil


class PandasUtil:

    @staticmethod
    def slowly_read_html(url):
        loop = True
        while loop:
            data_frame = PandasUtil.read_html(url)
            if data_frame:
                loop = False
        return data_frame

    @staticmethod
    def read_html(url,
                  header=None,
                  encoding="utf-8",
                  keep_default_na=False,
                  decimal=',',
                  thousands='.',
                  parse_dates=None):
        try:
            return pd.read_html(url,
                                header=header,
                                encoding=encoding,
                                keep_default_na=keep_default_na,
                                decimal=decimal,
                                thousands=thousands,
                                parse_dates=parse_dates)
        except:
            return False

    @staticmethod
    def read_file_csv(filename, usecols='ALL', encoding=None):

        if encoding:
            encoding = ManageFileUtil.get_file_encoding(filename)

        if usecols == 'ALL':
            return pd.read_csv(filename,
                               encoding=encoding,
                               sep=';',
                               header=0,
                               keep_default_na=False)

        df_ = pd.read_csv(filename, encoding=encoding, sep=';', header=0, usecols=usecols, keep_default_na=False)
        logging.info('PandasUtil read CSV with {} lines from {}'.format(len(df_), filename))
        return df_

    @staticmethod
    def new_data_frame(data=None, columns=None):
        return pd.DataFrame(data, columns=columns)

    @staticmethod
    def merge(left, right, how, on, suffixes):
        updated_df = pd.merge(left, right, how=how, on=on, suffixes=suffixes)
        columns_to_drop = list(filter(lambda x: (str(x).endswith('_old')), updated_df.columns))
        print(columns_to_drop)
        updated_df = updated_df.drop(columns=columns_to_drop)
        updated_df.reset_index(drop=True)
        return updated_df

# if __name__ == '__main__':
# data = {'key1' : ['t1', 't2', 't3'], 'key2':['a1', 'a2', 'a3']}
# data['key1'].append('t4')
# data['key2'].append('a4')
# df = pd.DataFrame(data)
# print(df)
