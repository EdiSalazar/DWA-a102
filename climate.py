# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 13:02:41 2021

@author: Edi
"""

#  Database of P from 2000-2020
#  ETp is stimated as a fraction of P
# Source:  https://opendata.dwd.de/climate_environment/CDC/regional_averages_DE/annual/
climate_dict = {
    'Brandenburg/Berlin' : [584, 365 ],
    'Brandenburg' : [584, 365 ],
    'Baden-Wuerttemberg' : [939, 587 ],
    'Bayern' : [926, 579 ],
    'Hessen' : [755, 472 ],
    'Mecklenburg-Vorpommern' : [621, 388 ],
    'Niedersachsen' : [755, 472 ],
    'Niedersachsen/Hamburg/Bremen' : [755, 472 ],
    'Nordrhein-Westfalen' : [855, 534 ],
    'Rheinland-Pfalz' : [764, 477 ],
    'Schleswig-Holstein' : [816, 510 ],
    'Saarland' : [893, 558 ],
    'Sachsen' : [723, 452 ],
    'Sachsen-Anhalt' : [575, 359 ],
    'Thueringen/Sachsen-Anhalt' : [636, 398 ],
    'Thueringen' : [714, 446 ],
    'Deutschland' : [785, 491 ],
}

def climate(place):
    return f"{climate_dict[place][0]}, {climate_dict[place][1]}"