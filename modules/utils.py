#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 12:37:21 2022

@author: anna chepaikina
"""
import pandas as pd

def flatten(A):
	rt = []
	for i in A:
		if isinstance(i,list): rt.extend(flatten(i))
		else: rt.append(i)
	return rt

def load_csv(fic, sep, header):
    df = pd.read_csv(fic, sep=sep, header=header)
    return df
