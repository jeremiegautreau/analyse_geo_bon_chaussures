from Geocoding import geocoding
from Analyse_geo_distance import analyse_geo_distance
from Analyse_geo_commune import analyse_geo_com
import os

def main():
    path_add = os.getenv('DATA_PATH')
    path_intersport = os.getenv('INTERSPORT_PATH')
    path_com = os.getenv('PATH_COM')
    path_France = os.getenv('PATH_FRANCE')
    col_add = 'Adresse clean'
    geo_add, status = geocoding(path_add, col_add)


    analyse_geo_distance(geo_add, path_intersport, path_France)

    analyse_geo_com(geo_add, path_com)


if __name__ == '__main__':
    main()
