# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:44:37 2021

@author: carlosGuevara
"""

# install git
# conda install pip
# pip install git+https://github.com/woodcrafty/PyETo#egg=PyETo
import numpy as np
import pandas as pd
import pyeto as pyeto
from pyeto import thornthwaite, monthly_mean_daylight_hours, deg2rad


from check import *
from coefficients import *
#%% Berechnungsansatz B.3.1: Steildach (alle Deckungsmaterialien),
#### Flachdach (Metall, Glas)  
def steep_roof(Area, P, ETp, Sp = 0.3):
    '''
    Calculates steep roof coefficients
    
    Parameters
    ----------
    Area : float
         element area in m2       
    
    P : float
      precipitation in mm/a
      
    ETp : float
        evapotranspiration in mm/yr
    
    Sp : float
       storage height in mm
       default: 0.3
       
    Notes    
    ------
    Storage height (Sp) in roofs varies between 0.1 and 0.6 mm. 
    Standard storage value for steep roof in general is 0.3 mm, 
    in case of glass or metal cover use 0.6 mm
    
    Returns
    -------
    df : DataFrame 
    '''  
    # check physical ranges from input values
    validRange(P, 'p')
    validRange(ETp, 'Etp')
    validRange(Sp, 'Sp')
    
    # calculate a coefficient          
    a = a_steepRoof(P, ETp, Sp)
    g = 0
    v = 1-a-g
    RD = P*a
    GWN = P*g
    ETP = P*v
    inflow = Area*P / 1000
    Q_RD = Area*P*a / 1000
    Q_GWN = Area*P*g / 1000
    Q_ETP = Area*P*v / 1000    
    # pfractions = (a, g, v)
    results = [{'Name' : "Area", 'Unit': "m2", 'Value': Area},
               {'Name' : "P", 'Unit': "mm/a", 'Value': P,},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETp},
               {'Name' : "a", 'Unit': "-", 'Value': a},
               {'Name' : "g", 'Unit': "-", 'Value': g},
               {'Name' : "v", 'Unit': "-", 'Value': v},
               {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
               {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
               {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
               {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
               {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
               {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
               {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
    results = pd.DataFrame(results)
    results.Value = results.Value.round(3)
    return(results)


if __name__ == "__main__":
    r = steep_roof(Area=1000, P=550, ETp=500)
    mmdlh = pyeto.monthly_mean_daylight_hours(pyeto.deg2rad(52.38), 2014)
    monthly_t = [3.1, 3.5, 5.0, 6.7, 9.3, 12.1, 14.3, 14.1, 11.8, 8.9, 5.5, 3.8]
    ETP_Thornthwaite = sum(pyeto.thornthwaite(monthly_t, mmdlh))
    steep_roof(Area = 1000, P = 800, ETp = ETP_Thornthwaite)

