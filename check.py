# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:18:57 2021

@author: carlosGuevara
"""


def precipitation(P):
    ''' raises an exception if precipitation range is not valid'''

    if ((P < 500) or (P > 1700)): 
        raise Exception('Precipitation value not valid. Valid range: 500 - 1700 mm/a')


def evapoTrans(Etp):
    ''' raises an exception if evapotranspiration range is not valid'''

    if ((Etp < 450) or (Etp > 700)): 
        raise Exception('Evapotranspiration value not valid. Valid range: (450 - 700 mm/a)')


def storageHeight(Sp):
    ''' raises an exception if storage height range is not valid'''

    if ((Sp < 0.1) or (Sp > 0.6)): 
        raise Exception('Storage height value not valid. Valid range: 0.1 - 0.6 mm')

     




    
    