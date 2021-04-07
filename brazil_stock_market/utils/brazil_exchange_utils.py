#!/usr/local/bin/python
# -*- coding: utf-8 -*-


class BrazilExchangeUtil:
    """
        Constant values for ISO 6166 and ISO 10962 used to identify the types of assets.
    """

    @staticmethod
    def reit_code() -> enumerate:
        """
            Define the local code for REIT identification
        :return:
        """
        return enumerate(dict({'ISIN': 'CTF', 'CFI': 'CI'}))

    @staticmethod
    def stock_code() -> enumerate:
        """
            Define local code to identify types of stock
        :return:
        """
        return enumerate({'ISIN': 'ACN|CDA', 'CFI_OR': 'OR', 'CFI_PR': 'PR'})

