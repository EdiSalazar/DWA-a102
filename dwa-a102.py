# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:42:52 2021

@author: Edi
"""

import numpy as np
import pandas as pd
from check_ranges import validRange
from climate import climate

#%% Starting class Surface

class Surface(object):
    # def __init__(self, p=800, etp=500, location=None):
    #     self.location = location        
    #     if self.location:
    #         p, etp = climate(self.location)
    #         self.p = p
    #         self.etp = etp
    #     else:
    #         self.p = p
    #         self.etp = etp

    #     validRange(self.p, 'P')
    #     validRange(self.etp, 'ETp')
               
    def __str__(self):
        return (
            f"Surface with precipitation of {self.p} mm/a,"
            f" and potential evapotranspiration of {self.etp} mm/a"
            )

#%% Berechnungsansatz A.2: Steildach Steildächer (alle Materialien), 
#### Flachdach (glatte Materialien) 

    def roof(self, area, sp=0.3):
        '''
        Calculates water balance components for steep roofs (all materials)
        or flat roofs made with smooth materials (e.g. glass, metal)
        
        Parameters
        ----------
        Area : float
             element area (m2)    
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
        
        Sp : float
           storage height (mm)
           
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P: 500 - 1700 mm/a
          ETp: 450 - 700 mm/a 
          Sp: 0.1 - 0.6 mm
          
        Standard Sp-values are:
          Steep roof: Sp = 0.3 mm
          Flat with smooth cover (glass or metal): Sp = 0.6 mm
        
        Returns
        -------
        results : DataFrame    
        '''    
        # validRange(self.p, 'P')
        # validRange(self.etp, 'ETp')
        validRange(sp, 'Sp_roof')
        
        a = (0.9115 + 0.00007063*self.p - 0.000007498*self.etp
             - 0.2063*np.log(sp + 1))
        g = 0
        v = 1-a-g
        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Roof', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}]
        
        results = pd.DataFrame(results)
        # results.Value = results.round(3)
        return(results)
    
    #%% Berechnungsansatz A.3: Flachdächer (raue Materialien, Kies), Asphalt,
    #### fugenloser Beton,Pflaster mit dichten Fugen
     
    def flat_area(self, area, sp=1):
        '''
        Calculates water balance components for flat roofs, asphalt, 
        jointless concrete, paving with tight joints.
        
        Parameters
        ----------
        Area : float
              element area (m2)
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
        
        Sp : float
            storage height (mm)
           
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a 
          Sp : 0.6 - 3 mm
          
        Standard Sp-values are:
          Flat roof with rough cover: Sp = 1
          Flat roof with gravel cover: Sp = 2
          Flat roof with asphalt or jointless concrete cover: Sp = 2.5
          Flat roof with plaster (tight joints) cover: Sp = 1.5
        
        Returns
        -------
        results : DataFrame   
        '''    
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(sp, 'Sp_flat_area') 
        
        a = (0.8658 + 0.0001659*self.p - 0.00009945*self.etp
             - 0.1542*np.log(sp + 1))
        g = 0
        v = 1-a-g
        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Flat area', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}]
        
        results = pd.DataFrame(results)
        # results.Value = results.round(3)
        return(results)
    
    #%% Berechnungsansatz A.4: Gründächer    
    def green_roof(self, area, h, kf=70, wkmax_wp=0.5):
        '''
        Calculates water balance components for green roofs
        
        Parameters
        ----------
        Area : float
              element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        h : float
          installation heigth (mm)
            
        kf : float 
            hydraulic conductivity (mm /h)  
        
        WKmax_WP : float
                  maximal water capacity (WKmax) minus wilting point (WP) (-)
                        
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a 
          h : 40 - 500 mm
          kf : 18 - 100 mm/h
          WKmax_WP : 0.35 - 0.65
          
        Standard values are:
          kf = 70 mm/h
          WKmax_WP = 0.5
              
        Returns
        -------
        results : DataFrame 
        '''       
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(h, 'h_green_roof')
        validRange(kf, 'kf_green_roof')
        validRange(wkmax_wp, 'WKmax_WP_green_roof')
        
        a = (-2.182 + 0.4293*np.log(self.p) - 0.0001092*self.p
             + (236.1/self.etp) + 0.0001142*h + 0.0002297*kf
             + 0.01628*np.log(wkmax_wp) - 0.1214*np.log(wkmax_wp*h))
        g = 0
        v = 1-a-g
        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Green foof', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}] 
        results = pd.DataFrame(results)
        return(results)
    
    #%% Berechnungsansatz A.5: Einstaudächer
    def storage_roof(self, area, sp=5):
        '''
        Calculates water balance components for storage roofs
        
        Parameters
        ----------
        Area : float
              element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        Sp : float
            storage height (mm)
                        
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a 
          Sp : 3 - 10 mm
          
        Standard Sp-value is:
          Sp : 5 mm
              
        Returns
        -------
        results : DataFrame 
        '''
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(sp, 'Sp_storage_roof') 
        
        a = 0.9231 + 0.000254*self.p - 0.0003226*self.etp - 0.1472*np.log(sp+1)
        g = 0
        v = 1-a-g 
        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Storage roof', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}]    
        results = pd.DataFrame(results)
        return(results)
        
    #%% Berechnungsansatz A.6 & A.7: Teildurchlässige Flächenbeläge
    ### (Fugenanteil 2 % bis 10 %)
    # Partially permeable surfaces (Joint ratio 2 % to 10 %)
    def permeable_surface(self, area, fa, kf, sp=1, wkmax_wp=0.15):
        '''
        Calculates water balance components for permeable surfaces
        
        Parameters
        ----------
        Area : float
              element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        FA :  float
            joint ratio of the pavers or partially permeable elements (%)
            
        kf : float 
            hydraulic conductivity (mm /h)
           
        Sp : float
            storage height (mm)
        
        WKmax_WP : float
                  maximal water capacity (WKmax) minus wilting point (WP) (-)
                        
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          FA : 2 - 10 %
          kf : 6 - 100 mm/h
          Sp : 0.1 - 2 mm
          WKmax_WP : 0.1 - 0.2
          
        Standard values are:
          Sp = 1 mm
          WKmax_WP = 0.15
          kf = 18 (if 2 <= FA < 6)
          kf = 36 (if 6 <= FA <= 10)
              
        Returns
        -------
        results : DataFrame 
        '''
        
    ### Berechnungsansatz A.6: Teildurchlässige Flächenbeläge
    ### (Fugenanteil 2 % bis 5 %)
    # Partially permeable surfaces (Joint ratio 2 % to 5 %)   
        if (fa >= 2 and fa <= 5):
            a = (0.0800734*np.log(self.p) - 0.0582828*fa - 0.0501693*sp
                  - 0.385767*wkmax_wp + (8.7040284/(11.9086896 + kf)))
            # DWA-a-102 2020 equation:
            # g = (-0.2006 - 0.000253*self.etp + 0.05615*fa - 0.0636*np.log(1 + sp)
            #      + 0.1596*np.log(1 + kf) + 0.2778*(wkmax_wp))
            v = (0.8529 - 0.1248*np.log(self.p) + 0.00005057*self.etp + 0.002372*fa
                  + 0.1583*np.log(1 + sp))
            # To fullfill the conservation mass (a+g+v=1). My decision is to apply:
            g = 1-a-v
    
    ### Berechnungsansatz A.7: Teildurchlässige Flächenbeläge
    ### (Fugenanteil 6 % bis 10 %)
    # Partially permeable surfaces (Joint ratio 6 % to 10 %)
    # This funtion can be joint with the previous one and add the param "slope"     
        if (fa >= 6 and fa <= 10):
            a = (0.05912*np.log(self.p) - 0.02749*fa - 0.03671*sp
                  - 0.30514*wkmax_wp + (4.97687/(4.7975 + kf)))
            # DWA-a-102 2020 equation:
            # g = (0.00004941*P - 0.0002817*self.etp + 0.02566*fa - 0.03823*sp
            #      + 0.691*np.exp(-6.465/kf))
            v = (0.9012 - 0.1325*np.log(self.p) + 0.00006661*self.etp + 0.002302*fa
                  + 0.1489*np.log(1 + sp))
            g = 1 - (a + v)
     
        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Permeable surface', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}]     
        results = pd.DataFrame(results)
        return(results)
        
    #%% Berechnungsansatz A.8: Teildurchlässige Flächenbeläge 
    #### (Poren- und Sickersteine, Schotterrasen, Kies)
    # Partially permeable surfaces
    # (pore stones, seepage stones), gravel surface, gravel lawn
    
    def porous_surface(self, area, sp=3.5, h=100, kf=180):
        '''
        Calculates water balance components for porous surfaces 
        (porous and percolating stones, gravel lawn)    
        
        Parameters
        ----------
        Area : float
              element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        Sp : float
            storage height (mm)
           
        h : float
          installation heigth (mm)
                   
        kf : float 
            hydraulic conductivity (mm /h)
                              
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          Sp : 2.5 - 4.2 mm
          h : 50 - 100 mm
          kf : 10 - 180 mm/h
          
        Standard values are:
          Sp = 3.5 mm
          h = 100 mm
          kf = 180 mm/h
              
        Returns
        -------
        results : DataFrame 
        '''
    
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(sp, 'Sp_porous_surface')
        validRange(h, 'h_porous_surface')
        validRange(kf, 'kf_porous_surface')
    
        a = (0.000001969*self.p - 0.005116*np.log(sp) - 0.0001051*h
              + 0.01753*np.exp(4.576/kf))
        # g = (0.2468883*np.log(self.p) - 0.0003938*self.etp + 0.0017083*sp
        #      - 0.0015998*h - 0.6703502*np.exp(0.1122885/kf))
        v = (0.2111 - 0.2544*np.log(self.p) + 0.2073*np.log(self.etp)
              + 0.0006249*sp + 0.123*np.log(h) - 0.000002806*kf)
        g = max((1 - (a + v)), 0.0) 
        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Porous surface', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}]     
        results = pd.DataFrame(results)
        return(results)
        
    #%% Berechnungsansatz A.9: Rasengittersteine
    # Paver stone grids / Grass pavers
    
    def paver_stonegrid(self, area, fa=25, sp=1, wkmax_wp=0.15):
        '''
        Calculates water balance components for paver stone grids
        
        Parameters
        ----------
        Area : float
              element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        FA :  float
            joint ratio of the pavers or partially permeable elements (%)
           
        Sp : float
            storage height (mm)
                   
        WKmax_WP : float
                  maximal water capacity (WKmax) minus wilting point (WP) (-)
                        
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          FA : 20 - 30 %
          Sp : 0.1 - 2 mm
          WKmax_WP : 0.1 - 0.2
          
        Standard values are:
          FA = 25 %
          Sp = 1
          WKmax_WP = 0.15
              
        Returns
        -------
        results : DataFrame 
        '''    
     
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(fa, 'FA_paver_stonegrid')
        validRange(sp, 'Sp_paver_stonegrid')
        validRange(wkmax_wp, 'WKmax_WP_paver_stonegrid') 
    
        a = (0.145704 - 0.059177*np.log(fa) - 0.007354*sp
              - 0.050531*np.log(wkmax_wp))
        # g = (- 0.02927 + 0.1483*np.log(self.p) - 0.000269*self.etp
        #      - 0.09913*np.log(1 + sp) + 0.05222*(wkmax_wp))
        v = (1.106 - 0.1625*np.log(self.p) + 0.0001282*self.etp
              + 0.1131*np.log(1 + sp) + 0.2848*wkmax_wp)
        g = max((1 - (a + v)), 0.0)

        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Paver stone-grid', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}]       
        results = pd.DataFrame(results)
        return(results)
        
    #%% Berechnungsansatz A.10: Deckschichten ohne Bindemittel (wassergebundene Decke) 
    # Wassergebundene Decke, offiziell Deckschicht ohne Bindemittel (Kürzel: DoB)
    # gravel ground cover
    
    def gravel_cover(self, area, h=100, sp=3.5, kf=1.8):
        '''
        Calculates water balance components for gravel covers or surfaces
        
        Parameters
        ----------
        Area : float
              element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        h : float
          installation heigth (mm)
        
        Sp : float
            storage height (mm)
                          
        kf : float 
            hydraulic conductivity (mm /h)
                        
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          h : 500 - 100 mm
          Sp : 2.5 - 4.2 mm
          kf : 0.72 - 10 mm/h
          
        Standard values are:
          h = 100 mm
          Sp = 3.5 mm
          kf : 1.8 mm/h
              
        Returns
        -------
        results : DataFrame 
        '''      
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(h, 'h_gravel_cover')
        validRange(sp, 'Sp_gravel_cover')
        validRange(kf, 'kf_gravel_cover')     
        
        a = 0.00004517*self.p - 0.03454*np.log(sp) + (0.1958/(0.2873 + kf))
        # g = (0.19761*np.log(self.p) - 0.000506*self.etp + 0.016372*sp - 0.001618*h
        #      - 0.327742*np.exp(0.346808/kf))
        v = (0.2111 - 0.2544*np.log(self.p) + 0.2073*np.log(self.etp)
              + 0.0006249*sp + 0.123*np.log(h) - 0.000002806*kf)
        g = max((1 - (a + v)), 0.0)
        e = 0
        # pfractions = (a, g, v)
        results = [{'Element' : 'Gravel cover', 'Area' : round(area, 3),
                    'Au' : round(area*a), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round(area*self.p*a/1000),
                    'Vg' : round(area*self.p*g/1000),
                    'Vv' : round(area*self.p*v/1000),
                    'Ve' : round(area*self.p*e/1000)}]       
        results = pd.DataFrame(results)
        return(results)
        
    #%% New class Measure
class Measure(object):
    # def __init__(self, *surfaces):
    #     # self.surfaces: surfaces
    #     pass
        
    def __str__(self):
        return "Measure to reduce runoff from the given surfaces"
    
    #%% Aufteilungswerte und Berechnungsansätze für Anlagen
    # Ableitung: Rohr, Rinne, steiler Graben
    # Drainage: pipe, channel, steep ditch
    
    def drainage(self, drainage_type, *surfaces):
        '''
        Calculates water balance components for drainage elements
        
        Parameters
        ----------
        Area : float
             element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        drainage_type : string
                       "pipe", "rohr", "channel", "rinne", "steep ditch",
                       "steiler graben", "ditch with vegetation",
                       "gräben mit bewuchs"
                        
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a   
              
        Returns
        -------
        results : DataFrame 
        '''    
     
        drainages = ("pipe", "Pipe", "PIPE", "Rohr", "rohr", "ROHR",
                     "channel", "Channel", "CHANNEL", "Rinne", "rinne",
                     "RINNE", "steep ditch", "Steep Ditch", "STEEP DITCH",
                     "steiler graben", "steiler Graben", "STEILER GRABEN")
        veg_drainage = ("Shallow ditches with vegetation",
                        "Ditch with vegetation", "ditch with vegetation",
                        "Flache Gräben mit Bewuchs", "Gräben mit Bewuchs")
    
        # validRange(self.p, 'P')
        # validRange(self.etp, 'ETp')
    
        if ((drainage_type in drainages) or
            (drainage_type in veg_drainage))  == False:
            return ("Wrong input as drinage-type")
        if (drainage_type in drainages) == True:   
            a = 1
            g = 0
            v = 0
        if (drainage_type in veg_drainage) == True:
            a = 0.7
            g = 0.1
            v = 0.2

        area = 0
        e = 0
        # calculating the area that produces runoff and volume of runoff
        au = 0
        va = 0
        for df in surfaces:
            au += float(df[-1:]['Au'])
            va += float(df[-1:]['Va'])
            
        # A df with the previous results is required
        previous_results = pd.DataFrame(columns = ['Element', 'Area', 'Au',
                                                   'P', 'Etp','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
                
        # Joinning previous dfs of results
        for df in surfaces:
            previous_results = pd.concat([previous_results, df])
            
        # Runoff volume are passed to measure so, Va = 0
        previous_results.Va = 0                      

        results = [{'Element' : 'Drainage', 'Area' : round(area),
                    'Au' : au, 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': area*self.p/1000,
                    'Va' : (area*self.p/1000 + va)*a,
                    'Vg' : (area*self.p/1000 + va)*g,
                    'Vv' : (area*self.p/1000 + va)*v,
                    'Ve' : (area*self.p/1000 + va)*e}]      
        results = pd.DataFrame(results)
        return(pd.concat([previous_results, results]))
    
    #%% Berechnungsansatz B.2: Flächenversickerung
    # Surface infiltration
    def surf_infiltration(self,  kf, *surfaces, fasf="fasf_standard"):
        '''
        Calculates water balance components for surface infiltration
        
        Parameters
        ----------
        Area : float
             element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        kf : float 
           hydraulic conductivity (mm /h)
           
        FAsf : float
            percentage of infiltration area (%)
                            
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          kf : 325 - 1100 mm/h
          FAsf : 66394*kf*exp(-1.197) - 70910*kf*exp(-1.117) (%)
          
        Standard values are:
          fasf_standard = 94741*kf*exp(-1.195)
              
        Returns
        -------
        results : DataFrame 
        '''
        
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(kf, 'kf_surf_infiltration') 
        
        if (fasf == "fasf_standard"):
            fasf = 94741*kf**(-1.195)
            fasf = 94741*kf**(-1.195)
            
        a = 0.004264 + 0.001121*np.log(self.p) - 0.002757*np.log(fasf)
        # g = (0.6207904 + 0.0899322*np.log(self.p) - 0.0001152*self.etp
        #      - 0.0719723*np.log(self.fasf))
        v = 0.3999 - 0.09317*np.log(self.p) + 0.00009746*self.etp + 0.07474*np.log(fasf)
        g = max((1 - (a + v)), 0.0)              
        e = 0
        
        # calculating the area that produces runoff and volume of runoff
        au = 0
        va = 0
        for df in surfaces:
            au += float(df[-1:]['Au'])
            va += float(df[-1:]['Va'])
            
        # A df with the previous results is required
        previous_results = pd.DataFrame(columns = ['Element', 'Area', 'Au',
                                                   'P', 'Etp','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
                
        # Joinning previous dfs of results
        for df in surfaces:
            previous_results = pd.concat([previous_results, df])
            
        # Runoff volume are passed to measure, Va = 0
        previous_results.Va = 0                      

        area = au*(fasf/100)

        results = [{'Element' : 'Surface infilt.', 'Area' : round(area),
                    'Au' : round(au), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round((area*self.p/1000 + va)*a),
                    'Vg' : round((area*self.p/1000 + va)*g),
                    'Vv' : round((area*self.p/1000 + va)*v),
                    'Ve' : round((area*self.p/1000 + va)*e)}]        
        results = pd.DataFrame(results)
        return(pd.concat([previous_results, results]))
       
    #%% Berechnungsansatz B.3: Versickerungsmulden
    # Infiltration swale
    def infilt_swale(self, kf, *surfaces, fasm="fasm_standard"):
        '''
        Calculates water balance components for infiltration swales
        
        Parameters
        ----------
        Area : float
             element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        kf : float 
           hydraulic conductivity (mm /h)
           
        FAsm : float
            percentage of infiltration area (%)
                            
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          kf : 14 - 3600 mm/h
          FAsf : 27.14*kf*exp(-0.303) - 62.414*kf*exp(-0.328) (%)
          
        Standard values are:
          FAsf_standard = 42.323*kf*exp(-0.314)
              
        Returns
        -------
        results : DataFrame 
        '''  
    
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        # validRange(kf, 'kf_infilt_swale') 
        
        if (fasm == "fasm_standard"):
            fasm = 42.323*kf**(-0.314)       
        
        g = (0.8608 + 0.02385*np.log(self.p) - 0.00005331*self.etp - 0.002827*fasm
              - 0.000002493*kf + 0.0009514*np.log(kf/fasm))
        v = 0.000008562*self.etp + (2.611/(self.p-64.35))*fasm**0.9425 - 0.000001211*kf
        # a = 1 - g - v
        # To force positive values or zero
        a = max((1 - (g + v)), 0.0)
        e = 0
        
        # calculating the area that produces runoff and volume of runoff
        au = 0
        va = 0
        for df in surfaces:
            au += float(df[-1:]['Au'])
            va += float(df[-1:]['Va'])
            
        # A df with the previous results is required
        previous_results = pd.DataFrame(columns = ['Element', 'Area', 'Au',
                                                   'P', 'Etp','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
                
        # Joinning previous dfs of results
        for df in surfaces:
            previous_results = pd.concat([previous_results, df])
            
        # Runoff volume are passed to measure, Va = 0
        previous_results.Va = 0                      

        area = au*(fasm/100)

        results = [{'Element' : 'Infilt. swale', 'Area' : round(area),
                    'Au' : round(au), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round((area*self.p/1000 + va)*a),
                    'Vg' : round((area*self.p/1000 + va)*g),
                    'Vv' : round((area*self.p/1000 + va)*v),
                    'Ve' : round((area*self.p/1000 + va)*e)}]        
        results = pd.DataFrame(results)
        return(pd.concat([previous_results, results]))
    #%% Berechnungsansatz B.4: Mulden-Rigolen-Elemente
    # Swale-trench element
    def swale_trench(self, kf, *surfaces, fasm="fasm_standard"):
        '''
        Calculates water balance components for swale-trench elements
        
        Parameters
        ----------
        Area : float
             element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        kf : float 
           hydraulic conductivity (mm /h)
           
        FAsm : float
            percentage of infiltration area (%)
                            
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          kf : 3.6 - 36 mm/h
          FAsf : 14.608*kf*exp(-0.406) - 47.634*kf*exp(-0.438) (%)
          
        Standard values are:
          FAsf_standard = 21.86*kf*exp(-0.348)
              
        Returns
        -------
        results : DataFrame 
        ''' 
    
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(kf, 'kf_swale_trench')
        
        if (fasm == "fasm_standard"):
            fasm = 21.86*kf**(-0.348)
            
        a = (-0.03867 + 0.007684*np.log(self.p) + 0.000003201*fasm + 0.0002564*kf
             - 0.0001187*fasm*kf + 0.004161*np.log(kf/fasm))
        # g = (0.8803 + 0.01866*np.log(self.p) - 0.00004867*self.etp
        #      - 0.001997*fasm + 0.0002365*kf)
        v = 0.000008879*self.etp + (2.528/(self.p-81.65))*fasm**0.9496 - 0.00007768*kf
        g = max((1 - (a + v)), 0.0)
        e = 0
        
        # calculating the area that produces runoff and volume of runoff
        au = 0
        va = 0
        for df in surfaces:
            au += float(df[-1:]['Au'])
            va += float(df[-1:]['Va'])
            
        # A df with the previous results is required
        previous_results = pd.DataFrame(columns = ['Element', 'Area', 'Au',
                                                   'P', 'Etp','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
                
        # Joinning previous dfs of results
        for df in surfaces:
            previous_results = pd.concat([previous_results, df])
            
        # Runoff volume are passed to measure, Va = 0
        previous_results.Va = 0                      

        area = au*(fasm/100)

        results = [{'Element' : 'Swale trench', 'Area' : round(area),
                    'Au' : round(au), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round((area*self.p/1000 + va)*a),
                    'Vg' : round((area*self.p/1000 + va)*g),
                    'Vv' : round((area*self.p/1000 + va)*v),
                    'Ve' : round((area*self.p/1000 + va)*e)}]   
        results = pd.DataFrame(results)
        return(pd.concat([previous_results, results]))
    
    #%% Berechnungsansatz B.5: Mulden-Rigolen-Systeme
    # Swale-trench system
    def swale_trench_system(self, qdr, kf, *surfaces, fasm="fasm_standard"):
        '''
        Calculates water balance components for swale-trench elements
        
        Parameters
        ----------
        Area : float
             element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        qDr : float
            throttled discharge yield (l/(s*ha))
            
        kf : float 
           hydraulic conductivity (mm /h)
           
        FAsf : float
            percentage of infiltration area (%)
                            
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          qDr : 1 - 10 l/(s*ha)
          kf : 0.36 - 3.6 mm/h
          FAsf : -
          
        Standard values are:
          FAsf_standard = 11.79 - 3.14*LN(qDr) - 0.18594*kf
              
        Returns
        -------
        results : DataFrame 
        ''' 
    
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(qdr, 'qDr_swale_trench_system')
        validRange(kf, 'kf_swale_trench_system')
        
        
        if (fasm == "fasm_standard"):
            fasm = 11.79 - 3.14*np.log(qdr) - 0.18594*kf
            
        a = (0.8112 + 0.0003473*self.p - 0.00001845*self.etp - 0.04793*fasm
              + 0.0007481*qdr - 0.4389*np.log(kf + 1))
        # g = (1.669 - 0.3005*np.log(self.p) - 0.00006933*self.etp
        #       + 0.3044*np.log(fasm) + 0.4581*np.log(kf + 1))
        v = (0.1428 - 0.02661*np.log(self.p) + 0.00005668*self.etp + 0.0288*np.log(fasm)
              - 0.0001825*qdr - 0.01823*np.log(kf + 1))
        g = max((1 - (a + v)), 0.0)
        e = 0
        
        # calculating the area that produces runoff and volume of runoff
        au = 0
        va = 0
        for df in surfaces:
            au += float(df[-1:]['Au'])
            va += float(df[-1:]['Va'])
            
        # A df with the previous results is required
        previous_results = pd.DataFrame(columns = ['Element', 'Area', 'Au',
                                                   'P', 'Etp','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
                
        # Joinning previous dfs of results
        for df in surfaces:
            previous_results = pd.concat([previous_results, df])
            
        # Runoff volume are passed to measure, Va = 0
        previous_results.Va = 0                      

        area = au*(fasm/100)

        results = [{'Element' : 'Swale trench system', 'Area' : round(area),
                    'Au' : round(au), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round((area*self.p/1000 + va)*a),
                    'Vg' : round((area*self.p/1000 + va)*g),
                    'Vv' : round((area*self.p/1000 + va)*v),
                    'Ve' : round((area*self.p/1000 + va)*e)}]
        results = pd.DataFrame(results)
        return(pd.concat([previous_results, results]))
    
    #%% Berechnungsansatz B.6: Anlagen zur Niederschlagswassernutzung
    # Rainwater usage
    def rainwater_usage(self, vsp, vbr, *surfaces, fabw=2, qbw=60):
        '''
        Calculates water balance components for rainwater usage
        
        Parameters
        ----------
        Area : float
             element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        VSp : float
            Specific storage volume (mm)
            
        VBr : float
            Available water volume to use in relation to the connected,
            effective runoff area (mm/d)
            
        FAbw : float 
             proportion of irrigated area in relation to the connected,
             effective runoff area (-)
           
        qBw : float
            specific annual requirement for irrigation l/(m^2*a)
                            
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          VSp : 10 - 200 mm
          VBr : 0 - 5 mm/d
          FAbw : 0 - 5
          qBw : 0 - 200 l/(m^2*a)
          
        Standard values are:
          FAbw = 2
          qBw = 60 l/(m^2*a)
              
        Returns
        -------
        results : DataFrame 
        '''     
        
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(vsp, 'VSp_rainwater_usage')
        validRange(vbr, 'VBr_rainwater_usage')
        validRange(fabw, 'FAbw_rainwater_usage')
        validRange(qbw, 'qBw_rainwater_usage')
        
        
        VBw = fabw*qbw
        Vnmin = min(self.p, 365*vbr + VBw)
        if VBw == 0:
            v = 0
        else:
            v = (- 0.0001927*self.p + 0.0001831*self.etp + 0.0006083*VBw
                 - 0.0000003127*VBw**2 - 0.3092*np.exp(3.269/vsp)
                 + (1.424/(2.782 + vbr)) + 0.0001885*Vnmin)
        if vbr == 0:
            e = 0
        else:
            e = (0.4451 - 0.0003529*self.p - 0.00007728*self.etp + 0.06821*np.log10(vsp)
                 - 0.0002507*VBw + 0.2349*np.log10(vbr) + 0.0001738*Vnmin)
        a = max((1 - (v + e)), 0.0)
        g = 0.0
        
        # calculating the area that produces runoff and volume of runoff
        au = 0
        va = 0
        for df in surfaces:
            au += float(df[-1:]['Au'])
            va += float(df[-1:]['Va'])
            
        # A df with the previous results is required
        previous_results = pd.DataFrame(columns = ['Element', 'Area', 'Au',
                                                   'P', 'Etp','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
                
        # Joinning previous dfs of results
        for df in surfaces:
            previous_results = pd.concat([previous_results, df])
            
        # Runoff volume are passed to measure, Va = 0
        previous_results.Va = 0                      

        area = 0

        results = [{'Element' : 'Rainwater usage', 'Area' : round(area),
                    'Au' : round(au), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round((area*self.p/1000 + va)*a),
                    'Vg' : round((area*self.p/1000 + va)*g),
                    'Vv' : round((area*self.p/1000 + va)*v),
                    'Ve' : round((area*self.p/1000 + va)*e)}]
        results = pd.DataFrame(results)
        return(pd.concat([previous_results, results]))
    
    #%% Berechnungsansatz B.7: Wasserfläche mit Dauerstau
    #### Water surface with permanent storage  
    # Pond system with inflow from paved areas
    def pod_system(self, aw, A_1, a_1, *surfaces, A_2= 0, a_2= 0.0, A_3= 0, a_3= 0.0,
               A_4= 0, a_4= 0.0):
        '''
        Calculates water balance components for rainwater usage
        
        Parameters
        ----------
        Area : float
             element area (m2)      
        
        P : float
          precipitation (mm/a)
          
        ETp : float
            evapotranspiration (mm/a)
            
        Aw : float
            pod surface (m2)
            
        A_i, ... , A_n : float
                       Area i, which directs its runoff to the pond (m2)
                       
        a_i, ... , a_n : float
                       proportion of area i (0.0-1.0), which directs its
                       runoff to the pond (-) 
                            
        Notes    
        ------
        Ranges of validity for the paremeters are:
          P : 500 - 1700 mm/a
          ETp : 450 - 700 mm/a
          a_i : 0 - 1
                   
        Returns
        -------
        results : DataFrame 
        '''
        
        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
        validRange(a_1, 'a_1_pod_system')
        validRange(a_2, 'a_2_pod_system')
        validRange(a_3, 'a_1_pod_system')
        validRange(a_4, 'a_1_pod_system')
        
        v = ((self.etp*aw)/(self.p*(aw + A_1*a_1 + A_2*a_2
                                    + A_3*a_3 + A_4*a_4)))
        a = 1 - v
        g = 0
        e = 0
        # calculating the area that produces runoff and volume of runoff
        au = 0
        va = 0
        for df in surfaces:
            au += float(df[-1:]['Au'])
            va += float(df[-1:]['Va'])
            
        # A df with the previous results is required
        previous_results = pd.DataFrame(columns = ['Element', 'Area', 'Au',
                                                   'P', 'Etp','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
                
        # Joinning previous dfs of results
        for df in surfaces:
            previous_results = pd.concat([previous_results, df])
            
        # Runoff volume are passed to measure, Va = 0
        previous_results.Va = 0                      

        area = 0

        results = [{'Element' : 'Rainwater usage', 'Area' : round(area),
                    'Au' : round(au), 'P': self.p, 'Etp' : self.etp,
                    'a' : round(a, 3), 'g' : round(g, 3), 'v' : round(v, 3),
                    'e' : round(e, 3), 'Vp': round(area*self.p/1000),
                    'Va' : round((area*self.p/1000 + va)*a),
                    'Vg' : round((area*self.p/1000 + va)*g),
                    'Vv' : round((area*self.p/1000 + va)*v),
                    'Ve' : round((area*self.p/1000 + va)*e)}]
        
        results = pd.DataFrame(results)
        return(pd.concat([previous_results, results]))


#%% Starting class Surface
class StudyArea(Surface, Measure):
    def __init__(self, p=800, etp=500, location=None):
        self.location = location        
        if self.location:
            p, etp = climate(self.location)
            self.p = p
            self.etp = etp
        else:
            self.p = p
            self.etp = etp

        validRange(self.p, 'P')
        validRange(self.etp, 'ETp')
                   
    def __str__(self):
        return (
            f"Study area has a precipitation of {self.p} mm/a,"
            f" and potential evapotranspiration of {self.etp} mm/a"
            )

def watbal(*study_areas):
        '''
        Calculates water balance for a system compund of the ouputs from
        methods of StudyArea (Surfaces, Measures).
        
        Parameters
        ----------
        args : DataFrame 
             outputs of methods from StudyArea (Surfaces, Measures)  
                          
        Returns
        -------
        results : DataFrame 
        '''
        df_layout = pd.DataFrame(columns = ['Element', 'Area','a', 'g', 'v', 
                                                   'e', 'Vp', 'Va', 'Vg',
                                                   'Vv', 'Ve'])
        
        area, vp, va, vg, vv, ve = 0, 0, 0, 0, 0, 0
        for df in study_areas:
            area += float(sum(df[:]['Area']))
            vp += float(sum(df[:]['Vp']))
            va += float(sum(df[:]['Va']))
            vg += float(sum(df[:]['Vg']))
            vv += float(sum(df[:]['Vv']))
            ve += float(sum(df[:]['Ve']))
        a = round(va/vp, 3)
        g = round(vg/vp, 3)
        v = round(vv/vp, 3)
        e = round(ve/vp, 3)
        
        sys_results = [{'Element' : 'System', 'Area' : round(area),
                    'a' : a, 'g' : g, 'v' : v, 'e' : e, 'Vp': round(vp),
                    'Va' : round(va),'Vg' : round(vg),'Vv' : round(vv),
                    'Ve' : round(ve)}]
        
        sys_results = pd.DataFrame(sys_results)
        
        sys_results = pd.concat([df_layout, *study_areas, sys_results],
                                join= "inner")
        
        # this still need to be solved
        # delete column e and ve if all column is zero
        
        if (True in (sys_results.e.values != 0)) == False:
            sys_results = sys_results.drop(columns = ["e"])
            sys_results = sys_results.drop(columns = ["Ve"])
                    
        return(sys_results)