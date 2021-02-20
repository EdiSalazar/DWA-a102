# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:18:57 2021

@author: carlosGuevara
"""

_var = {'p': [500, 1700, 'Precipitation', ], 
        'Etp' :[450, 700, 'Evapotranspiration'], 
        'Sp': [0.1, 0.6, 'Water height'], 
        }


def validRange(val, param):
    ''' generic function to check parameter range'''
    
    if ( (val < _var[param][0]) or (val > _var[param][1]) ): 
        raise Exception(f'{_var[param][2]} value not valid. Valid range: {_var[param][0]} - {_var[param][1]} mm/a')
    





     




    
    