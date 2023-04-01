from Geocoding import geocoding
from Analyse_geo_distance import analyse_geo_distance


def main():

    path_add = 'C://Users//jerem//PycharmProjects//pythonProject//' \
            'analyse_geo_bon_chaussures//data//analyse_geo_add.csv'
    col_add = 'Adresse clean'

    geocoding(path_add, col_add)

    geo_add = df

    path_intersport = r'C:\Users\jerem\PycharmProjects\pythonProject\analyse_geo_bon_chaussures\data\analyse_geo_intersport.csv'

    analyse_geo_distance(geo_add, path_intersport)

    path_com = r'C:\Users\jerem\PycharmProjects\pythonProject\analyse_geo_bon_chaussures\data\2021-topo-comOnly-4326.json'




if __name__ == '__main__':
    main()
