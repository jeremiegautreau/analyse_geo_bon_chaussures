from Geocoding import geocoding
from Analyse_geo_distance import analyse_geo_distance
import os

def main():
    path_add = os.getenv('DATA_PATH')
    path_intersport = os.getenv('INTERSPORT_PATH')
    col_add = 'Adresse clean'
    geo_add, status = geocoding(path_add, col_add)

    analyse_geo_distance(geo_add, path_intersport)
    test = 7//2
    path_com = r'C:\Users\jerem\PycharmProjects\pythonProject\analyse_geo_bon_chaussures\data\2021-topo-comOnly-4326.json'


if __name__ == '__main__':
    main()
