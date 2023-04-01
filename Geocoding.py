
import requests
import pandas as pd
from io import StringIO


#path_add = 'C://Users//jerem//Bon chaussures//analyse_geo_add.csv'


def geocoding(path_add, col_add):

    url = 'https://api-adresse.data.gouv.fr/search/csv/'

    files = [
        ('data', open(path_add, 'rb')),
        ('columns', (None, col_add)),
        ('result_columns', (None, 'latitude')),
        ('result_columns', (None, 'longitude')),
        ('result_columns', (None, 'result_city')),
        ('result_columns', (None, 'result_citycode')),
    ]

    response = requests.post(url, files=files)

    if response.status_code == 200:
        status = 'Request successful'

        geocoded = response.content

        df = pd.read_csv(StringIO(geocoded.decode('utf-8')), sep=';')
        df['Utilise'].fillna(0, inplace=True)
        df.dropna(subset=['latitude', 'longitude'], inplace=True)

        return df, print(status)

    else:
        status = 'Error during request to API: '+str(response.status_code)

        return print(status)
