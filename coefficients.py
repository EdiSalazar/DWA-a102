# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 15:00:50 2021

@author: carlosGuevara
"""

import numpy as np


def a_steepRoof(P, ETp, Sp):
    
    '''Calculates a coefficient for steep roof'''
    
    return 0.9115 + 0.00007063*P - 0.000007498*ETp - 0.2063*np.log(Sp + 1)