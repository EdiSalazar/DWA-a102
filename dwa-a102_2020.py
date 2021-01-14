# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 10:05:35 2020
Following new DWA-102 (Dec. 2020)

@author: Edi
"""

import numpy as np

#%% Berechnungsansatz B.3.1: Steildach (alle Deckungsmaterialien),
#### Flachdach (Metall, Glas)  
def steeproof(P, ETp, Sp):
    '''storage height (Sp) in roofs varies between 0.1 and 0.6 mm. Recommended
    storage value for steep roof in general is 0.3 mm, in case of glass or
    metal cover use 0.6 mm
    '''
    a = 0.9115 + 0.00007063*P - 0.000007498*ETp - 0.2063*np.log(Sp + 1)
    g = 0
    v = 1-a-g
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(steeproof(450, 350, 0.3))
sum(steeproof(450, 350, 0.3))

#%% Berechnungsansatz B.3.2: Flachdach (Dachpappe, Faserzement, Kies),
#### Asphalt, fugenloser Beton, Pflaster mit dichten Fugen  
def flatroof(P, ETp, Sp):
    '''storage (Sp) in flat roofs varies between 0.6 and 3 mm. Recommended (Sp)
    values are:
    Flat roof with rough cover = 1;
    Flat roof with gravel cover = 2;
    Flat roof with asphalt or jointless concrete cover = 2.5;
    Flat roof with plaster (tight joints) cover = 1.5
    '''
    a = 0.8658 + 0.0001659*P - 0.00009945*ETp - 0.1542*np.log(Sp + 1)
    g = 0
    v = 1-a-g
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(flatroof(450, 350, 0.3))
sum(flatroof(450, 350, 0.3))

#%% Berechnungsansatz B.3.3: Gründach
def greenroof(P, ETp, h, kf, WKmax, WP):
    '''heigth (h) corresponds to the installation heigth of the green roof (mm),
    kf stands for hydraulic conductivity (mm/h), WKmax corresponds to
    maximal water capacity (-) and WP to wilting point (-). Recommended value
    for difference (WKmax - WP) is 0.5
    ''' 
    a = -2.182 + 0.4293*np.log(P) - 0.0001092*P + (236.1/ETp) + 0.0001142*h
    + 0.0002297*kf + 0.01628*np.log(WKmax - WP)
    - 0.1214*np.log((WKmax - WP)*h)
    g = 0
    v = 1-a-g
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(greenroof(450, 350, 100, 70, 0.8, 0.5))
sum(greenroof(450, 350, 100, 70, 0.8, 0.5))
#%% Berechnungsansatz B.3.4: Einstaudach (Speicherhöhe > 3mm)
def storageroof(P, ETp, Sp):
    ''' function for roofs with a storage heigth (Sp) desing bigger than 3 mm
    and lower than 10 mm. Recommended value for Sp = 5.
    '''
    a = 0.9231 + 0.000254*P - 0.0003226*ETp - 0.1472*np.log(Sp+1)
    g = 0
    v = 1-a-g
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(storageroof(450, 350, 5))
sum(storageroof(450, 350, 5))

#%% Berechnungsansatz B.3.5: Teildurchlässige Flächenbeläge
### (Fugenanteil 2 % bis 5 %)
# Partially permeable surfaces (Joint ratio 2 % to 5 %)
def partpearmsurf(P, ETp, FA, Sp, WKmax, WP, kf):
    '''FA corresponds to the joint ratio of the pavers or partially permable
    elements, and its recommended value is 4. The recommended storage heigth
    (Sp) is 1 mm. WKmax corresponds to maximal water capacity (-) and WP to
    wilting point (-). Recommended value for difference (WKmax - WP) is 0.15. 
    kf stands for hydraulic conductivity (mm/h)
    '''
    a = 0.0800734*np.log(P) - 0.0582828*FA - 0.0501693*Sp
    - 0.385767*(WKmax - WP) + (8.7040284/(11.9086896+kf))
    # DWA-a-102 2020 equation:
    # g = -0.2006 - 0.000253*ETp + 0.05615*FA - 0.0636*np.log(1 + Sp) + 0.1596*np.log(1 + kf) + 0.2778*(WKmax - WP)
    v = 0.8529 - 0.1248*np.log(P) + 0.00005057*ETp + 0.002372*FA + 0.1583*np.log(1 + Sp)
    # To fullfill the conservation mass (a+g+v=1). My decision is to apply:
    g = 1-a-v
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(partpearmsurf(650, 500, 4, 1, 0.35, 0.20, 18))
sum(partpearmsurf(650, 500, 4, 1, 0.35, 0.20, 18))


#%% Berechnungsansatz B.3.6: Teildurchlässige Flächenbeläge
### (Fugenanteil 6 % bis 10 %)
# Partially permeable surfaces (Joint ratio 6 % to 10 %)
# This funtion can be joint with the previous one and add the param "slope"
def partpearmsurf2(P, ETp, FA, Sp, WKmax, WP, kf):
    '''FA corresponds to the joint ratio of the pavers or partially permable
    elements, and its recommended value is 8. The recommended storage heigth 
    (Sp) is 1 mm. WKmax corresponds to maximal water capacity (-) and WP to
    wilting point (-). Recommended value for difference (WKmax - WP) is 0.15. 
    kf stands for hydraulic conductivity (mm/h)
    '''
    a = 0.05912*np.log(P) - 0.02749*FA - 0.03671*Sp - 0.30514*(WKmax - WP)
    + (4.97687/(4.7975 + kf))
    # g = 0.00004941*P - 0.0002817*ETp + 0.02566*FA - 0.03823*Sp + 0.691*np.exp(-6.465/kf)
    v = 0.9012 - 0.1325*np.log(P) + 0.00006661*ETp + 0.002302*FA + 0.1489*np.log(1 + Sp)
    g = 1 - (a + v)
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(partpearmsurf2(650, 500, 4, 1, 0.35, 0.20, 18))
sum(partpearmsurf2(650, 500, 4, 1, 0.35, 0.20, 18))

#%% Berechnungsansatz B.3.7: Teildurchlässige Flächenbeläge
### (Porensteine, Sickersteine), Kiesbelag, Schotterrasen
# Partially permeable surfaces
# (pore stones, seepage stones), gravel surface, gravel lawn
def partpearmsurf3(P, ETp, Sp, h, kf):
    '''recommended values are:
    storage heigth (Sp) = 3.5 mm
    installation heigth (h) of the surface = 100 mm
    '''
    a = 0.000001969*P - 0.005116*np.log(Sp) - 0.0001051*h + 0.01753*np.exp(4.576/kf)
    # g = 0.2468883*np.log(P) - 0.0003938*ETp + 0.0017083*Sp - 0.0015998*h - 0.6703502*np.exp(0.1122885/kf)
    v = 0.2111 - 0.2544*np.log(P) + 0.2073*np.log(ETp) + 0.0006249*Sp + 0.123*np.log(h) - 0.000002806*kf
    g = 1 - (a + v)
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(partpearmsurf3(1000, 650, 4, 100, 180))
sum(partpearmsurf3(1000, 650, 4, 100, 180))

#%% Berechnungsansatz B.3.8: Rasengittersteine
# Lawn grid stones / paver stone grids
def paverstonegrid(P, ETp, FA, Sp, WKmax, WP):
    '''FA corresponds to the joint ratio of the pavers or partially permable
    elements, and its recommended value is 25. The recommended storage heigth 
    (Sp) is 1 mm. WKmax corresponds to maximal water capacity (-) and WP to
    wilting point (-). Recommended value for difference (WKmax - WP) is 0.15. 
    kf stands for hydraulic conductivity (mm/h)
    '''
    a = 0.145704 - 0.059177*np.log(FA) - 0.007354*Sp - 0.050531*np.log(WKmax - WP)
    # g = - 0.02927 + 0.1493*np.log(P) - 0.000269*ETp - 0.09913*np.log(1 + Sp) + 0.05222*(WKmax - WP)
    v = 1.106 - 0.1625*np.log(P) + 0.0001282*ETp + 0.1131*np.log(1 + Sp) + 0.2848*(WKmax - WP)
    g = 1 - (a + v)
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(paverstonegrid(1000, 650, 25, 1, 0.30, 0.15))
sum(paverstonegrid(1000, 650, 25, 1, 0.30, 0.15))

#%% Berechnungsansatz B.3.9: Wassergebundene Decke
# Wassergebundene Decke, offiziell Deckschicht ohne Bindemittel (Kürzel: DoB)
# gravel ground cover
def gravelcover(P, ETp, h, Sp, kf):
    '''recommended values are:
    installation heigth (h) = 100 m
    storage heigth (Sp) = 3.5 mm
    '''
    a = 0.00004517*P - 0.03454*np.log(Sp) + (0.1958/(0.2873 + kf))
    # g = 0.19761*np.log(P) - 0.000506*ETp + 0.016372*Sp - 0.001618*h - 0.327742*np.exp(0.346808/kf)
    v = 0.2111 - 0.2544*np.log(P) + 0.2073*np.log(ETp) + 0.0006249*Sp + 0.123*np.log(h) - 0.000002806*kf
    g = 1 - (a + v)
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(gravelcover(1000, 650, 100, 3.5, 1.8))
sum(gravelcover(1000, 650, 100, 3.5, 1.8))

#%% Berechnungsansatz B.4 Aufteilungswerte und Berechnungsansätze für Anlagen
# Ableitung: Rohr, Rinne, steiler Graben
# Drainage: pipe, channel, steep ditch
def drainage(drainagetype):
    '''
    draingetype is a text input, the possible input options are:
    "pipe", "Pipe", "PIPE", "Rohr", "rohr", "ROHR", "channel","Channel",
    "CHANNEL", "Rinne", "rinne", "RINNE", "steep ditch", "Steep Ditch",
    "STEEP DITCH", "steiler graben","steiler Graben", "STEILER GRABEN",
    "Shallow ditches with vegetation", "Ditch with vegetation",
    "ditch with vegetation", "Flache Gräben mit Bewuchs","Gräben mit Bewuchs"
    '''
    drainages = ("pipe", "Pipe", "PIPE", "Rohr", "rohr", "ROHR", "channel",
                 "Channel", "CHANNEL", "Rinne", "rinne", "RINNE",
                 "steep ditch", "Steep Ditch", "STEEP DITCH", "steiler graben",
                 "steiler Graben", "STEILER GRABEN")
    veg_drainage = ("Shallow ditches with vegetation", "Ditch with vegetation",
                    "ditch with vegetation", "Flache Gräben mit Bewuchs",
                    "Gräben mit Bewuchs")
    #  The input could be change to a numeric value, like 1 = Rohr, Rinne..
    #  and 2 = Flache Gräben mit Bewuchs.
    if (drainagetype in drainages) == True:
        return (1, 0, 0)
    if (drainagetype in veg_drainage) == True:
        return (0.7, 0.1, 0.2)
    else:
        return ("Wrong input as drinage-type")
# Test
print(drainage("pipe"))
sum(drainage("pipe"))
print(drainage("ditch with vegetation"))
sum(drainage("ditch with vegetation"))
print(drainage("wrong name as test"))
# sum(drainage("wrong name as test"))

#%% Berechnungsansatz B.4.1: Flächenversickerung
# Surface infiltration
def surfinfiltration(P, ETp, FAsm, kf):
    '''FAsm (%) stands for percentage of infiltration area. The recommended value
    is calculated in terms of the hydraulic conductivity (mm/h) as:
    94741*kf*exp(-1.195)
    '''
    a = 0.004264 + 0.001121*np.log(P) - 0.002757*np.log(FAsm)
    # g = 0.6207904 + 0.0899322*np.log(P) - 0.0001152*ETp - 0.0719723*np.log(FAsm)
    v = 0.3999 - 0.09317*np.log(P) + 0.00009746*ETp + 0.07474*np.log(FAsm)
    g = 1 - (a + v)
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(surfinfiltration(1500, 700, 56.4, 500))
sum(surfinfiltration(1500, 700, 56.4, 500))

#%% Berechnungsansatz B.4.2: Versickerungsmulde
# Infiltration swale
def infiltswale(P, ETp, FAsm, kf):
    '''FAsm (%) stands for percentage of percolation area (swale). The 
    recommended value is calculated in terms of the hydraulic 
    conductivity (mm/h) as:
    42.323*kf*exp(-0.314)
    '''
    g = 0.8608 + 0.02385*np.log(P) - 0.00005331*ETp - 0.002827*FAsm
    - 0.000002493*kf + 0.0009514*np.log(kf/FAsm)
    v = 0.000008562*ETp + (2.611/(P-64.35))*FAsm**0.9425 - 0.000001211*kf
    a = 1 - g - v
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(infiltswale(1700, 700, 6, 500))
sum(infiltswale(1700, 700, 6, 500))
#%% Berechnungsansatz B.4.3: Mulde-Rigolen-Elemente
# Swale-trench element
def swale_trench(P, ETp, FAsm, kf):
    '''FAsm (%) stands for percentage of percolation area (swale). The
    recommended value is calculated in terms of the hydraulic
    conductivity (mm/h) as:
    21.86*kf*exp(-0.348)
    '''
    a = -0.03867 + 0.007684*np.log(P) + 0.000003201*FAsm + 0.0002564*kf
    - 0.0001187*FAsm*kf + 0.004161*np.log(kf/FAsm)
    # g = 0.8803 + 0.01866*np.log(P) - 0.00004867*ETp - 0.001997*FAsm + 0.0002365*kf
    v = 0.000008879*ETp + (2.528/(P-81.65))*FAsm**0.9496 - 0.00007768*kf
    g = 1 - (a + v)
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(swale_trench(1500, 700, 6, 12))
sum(swale_trench(1500, 700, 6, 12))


#%% Berechnungsansatz B.4.4: Mulden-Rigolen-System
# Swale-trench system
def swale_trench_system(P, ETp, FAsm, qDr, kf):
    '''FAsm stands for percentage of percolation area (swale), and qDr for
    Throttled discharge yield (l/(s*ha)). The recommended BAsm value is
    calculated in terms of the hydraulic conductivity kf (mm/h) and qDr as:
    11.79 - 3.14*LN(qDR) - 0.18594*kf
    '''
    a = 0.8112 + 0.0003473*P - 0.00001845*ETp - 0.04793*FAsm + 0.0007481*qDr
    - 0.4389*np.log(kf + 1)
    # g = 1.669 - 0.3005*np.log(P) - 0.00006933*ETp + 0.3044*np.log(FAsm) + 0.4581*np.log(kf + 1)
    v = 0.1428 - 0.02661*np.log(P) + 0.00005668*ETp + 0.0288*np.log(FAsm)
    - 0.0001825*qDr - 0.01823*np.log(kf + 1)
    g = 1 - (a + v)
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(swale_trench_system(1500, 700, 5.8, 6, 2))
sum(swale_trench_system(1500, 700, 5.8, 6, 2))


#%% Berechnungsansatz B.4.5: Regenwassernutzung
# Rainwater usage
def rainwater_usage(P, ETp, VSp, VBr, VBw1, VBw2):
    '''VSp stands for Specific storage volume in relation to the connected,
    flow-effective area (mm).
    VBr correspond to the available water volume to use in relation to the
    connected, effective runoff area (mm/d).
    VBw1 corresponds to proportion of irrigated area in relation to the
    connected area, effective runoff area (-).
    VBw2 stands for Specific annual requirement for irrigation (l/(m^2*a))
    '''
    VBw = VBw1*VBw2
    Vnmin = min(P, 365*VBr + VBw)
    if VBw == 0:
        v = 0
    else:
        v = - 0.0001927*P + 0.0001831*ETp + 0.0006083*VBw - 0.0000003127*VBw**2
        - 0.3092*np.exp(3.269/VSp) + (1.424/(2.782 + VBr)) + 0.0001885*Vnmin
    if VBr == 0:
        e = 0
    else:
        e = 0.4451 - 0.0003529*P - 0.00007728*ETp + 0.06821*np.log10(VSp)
        - 0.0002507*VBw + 0.2349*np.log10(VBr) + 0.0001738*Vnmin
    a = 1 - (v + e)
    pfractions = (a, e, v)
    return(pfractions)

# Test
print(rainwater_usage(1500, 700, 100, 3, 2, 60))
sum(rainwater_usage(1500, 700, 100, 3, 2, 60))

#%% Berechnungsansatz B.4.6: Teichanlage mit Zufluss von befestigten Flächen
# # Pond system with inflow from paved areas
def pod_system(P, ETp, Aw, *Azui_aui):
    '''Aw stands for pod surface (m2),
    A_i corresponds to the Area i, which directs its runoff to the pond (m2),
    a_i corresonds to proportion of area i (0.0-1.0), which directs its runoff
    to the pond (-)
    '''
    if len(Azui_aui)%2 != 0:
        return("Every area that produce runoff should have its associate proportion area that produces runoff")
    else:
        partialarea = 0
        for i in range(0, len(Azui_aui), 2):
            partialarea = partialarea + Azui_aui[i]*Azui_aui[i+1]      
    v = (ETp*Aw)/(P*(Aw + partialarea))
    a = 1 - v
    g = 0
    pfractions = (a, g, v)
    return(pfractions)
print(pod_system(1500, 700, 100, 10, 0.5, 15, 0.6, 20, 0.8))
sum(pod_system(1500, 700, 100, 10, 0.5, 15, 0.6, 20, 0.8))

#%% Berechnungsansatz B.4.6: Teichanlage mit Zufluss von befestigten Flächen
# Pond system with inflow from paved areas
def pod_system(P, ETp, Aw, A_1, a_1, A_2= 0, a_2= 0.0, A_3= 0, a_3= 0.0,
               A_4= 0, a_4= 0.0):
    '''Aw stands for pod surface (m2),
    A_i corresponds to the Area i, which directs its runoff to the pond (m2),
    a_i corresonds to proportion of area i (0.0-1.0), which directs its runoff
    to the pond (-)
    '''   
    v = (ETp*Aw)/(P*(Aw + A_1*a_1 + A_2*a_2 + A_3*a_3 + A_4*a_4))
    a = 1 - v
    g = 0
    pfractions = (a, g, v)
    return(pfractions)

# Test
print(pod_system(1500, 700, 100, 10, 0.5, 15, 0.6, 20, 0.8))
sum(pod_system(1500, 700, 100, 10, 0.5, 15, 0.6, 20, 0.8))
