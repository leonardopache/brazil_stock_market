#!/usr/local/bin/python
# -*- coding: utf-8 -*-


def split_array(num_sub_arr, array) -> list:
    """
        Utility to split an array in x sub-array.

    :param num_sub_arr: 
    :param array: 
    :return: new array with content x sub-arrays
    """
    size = len(array)
    split_size = int(size / num_sub_arr)
    ini = 0
    pivot = 0
    arr = []
    for i in range(num_sub_arr - 1):
        pivot += split_size
        arr.append(array.iloc[ini:pivot])
        ini = pivot
    arr.append(array.iloc[ini:])
    return arr
