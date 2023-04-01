import requests
import pandas as pd
from io import StringIO

DEFAULT_REQUEST = [
    ('result_columns', (None, 'latitude')),
    ('result_columns', (None, 'longitude')),
    ('result_columns', (None, 'result_city')),
    ('result_columns', (None, 'result_citycode')),
]


def format_geocoded_data(geocoded_data):
    df = pd.read_csv(StringIO(geocoded_data.decode('utf-8')), sep=';')
    df['Utilise'].fillna(0, inplace=True)
    df.dropna(subset=['latitude', 'longitude'], inplace=True)
    return df


def geocoding(path_add, col_add, files=DEFAULT_REQUEST):
    files = [('data', open(path_add, 'rb')),
             ('columns', (None, col_add))
             ] + files
    url = 'https://api-adresse.data.gouv.fr/search/csv/'
    response = requests.post(url, files=files)

    if response.status_code == 200:
        status = 'Request successful'
        geocoded = response.content
        df = format_geocoded_data(geocoded)
        return df, status
    else:
        status = 'Error during request to API: ' + str(response.status_code)
        return None, status


if __name__ == '__main__':
    pass
