#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 12:37:21 2022

@author: anna chepaikina
"""
import pandas as pd

def flatten(A):
    """
    

    Parameters
    ----------
    A : list of lists
        nested list.

    Returns
    -------
    rt : list
        flat list.

    """
    
    rt = []
    for i in A:
        if isinstance(i,list): rt.extend(flatten(i))
        else: rt.append(i)
    return rt

def load_csv(fic, sep, header):
    """
    

    Parameters
    ----------
    fic : str
        path to the csv file.
    sep : str
        separator between the columns.
    header : 0, or None
        0 if first row has names of columns
        None if it doesn't.

    Returns
    -------
    df : object
        dataframe, containing columns from the cqv file.

    """
    df = pd.read_csv(fic, sep=sep, header=header)
    return df


def index_exists(ls, i):
    """
    

    Parameters
    ----------
    ls : list
        list of elements.
    i : str
        index to verify.

    Returns
    -------
    True
        if index exists in the list.

    """
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)