#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from ..utils.pandas_util import PandasUtil


class ManagerCIA:
    """
        Class responsible for keep the market information updated in internal data base
    """
    @staticmethod
    def load_info_into_dataframe(csv_file):
        """
            Based on .csv normalize only relevant information and add to memory dataframe.
        :return:
            cias_df
        """
        cia_cad_df = PandasUtil.read_file_csv(csv_file, encoding='ISO-8859-1',
                                              usecols=['CNPJ_CIA', 'DENOM_SOCIAL', 'DT_REG', 'CD_CVM', 'SIT',
                                                       'SIT_EMISSOR', 'MUN'])
        cia_cad_df = cia_cad_df.loc[cia_cad_df['SIT'] == 'ATIVO']
        cia_cad_df = cia_cad_df.reset_index(drop=True)

        return cia_cad_df
