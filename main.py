from Geocoding import geocoding
from Analyse_geo_distance import analyse_geo_distance
from Analyse_geo_commune import analyse_geo_com
import os

def main():
    path_add = os.getenv('DATA_PATH')
    path_intersport = os.getenv('INTERSPORT_PATH')
    path_com = r'C:\Users\jerem\PycharmProjects\pythonProject\analyse_geo_bon_chaussures\data\2021-topo-comOnly-4326.json'
    col_add = 'Adresse clean'
    geo_add, status = geocoding(path_add, col_add)

    analyse_geo_distance(geo_add, path_intersport)

    analyse_geo_com(geo_add, path_com)


if __name__ == '__main__':
    main()
