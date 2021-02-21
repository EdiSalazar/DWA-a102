# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:42:52 2021

@author: Edi
"""

import numpy as np
import pandas as pd
from check_ranges import validRange


#%% Starting classes

class Surface(object):
    def __init__(self, area, p, etp, sp=0, h=0, kf=0, wkmax_wp=0, fa=0):
        self.area = area
        self.p = p
        self.etp = etp
        self.sp = sp
        self.h = h
        self.kf = kf
        self.wkmax_wp = wkmax_wp
        self.fa = fa
        
    def __str__(self):
        return (
            f"Surface with area: {self.area} m2, precipitation of {self.p} mm/a,"
            f" and potential evapotranspiration of {self.etp} mm/a"
            )
    
        