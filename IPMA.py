# This module performs a request to the IPMA API
# which returns the weather prediction for 3 days
# The day is passed as a parameter to the API call
# It only returns the rain probability, max and min temperatures
import requests

def chamadaAPI(dia):
    # Dia: 0 - Hoje | 1 - Amanhã | 2 - Depois de amanhã
    url = 'https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/hp-daily-forecast-day' + str(dia) + '.json'
    response = requests.get(url)
    tempo = response.json()

    return (meteorologia(tempo))

def meteorologia(tempo):
    casteloBrancoID = 1050200
    guardaID = 1090700

    CB = []
    GD = []

    for t in tempo['data']:
        if t["globalIdLocal"] == casteloBrancoID:
            CB = t
        elif t["globalIdLocal"] == guardaID:
            GD = t
        else:
            pass
    
    chuvaCB = CB['precipitaProb']
    minCB = CB['tMin']
    maxCB = CB['tMax']

    chuvaGD = GD['precipitaProb']
    minGD = GD['tMin']
    maxGD = GD['tMax']

    chuva = float(chuvaCB) + float(chuvaGD)
    tMin = (minCB + minGD) / 2
    tMax = (maxCB + maxGD) / 2
    
    return chuva, tMin, tMax

__version__ = '0.1'
