# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 15:39:46 2024

@author: 213
"""

API_KEY = '4d6b43495864736537377145565341'

import pandas as pd

def load_data():
    data = pd.read_csv('seoul_real_estate.csv')
    return data