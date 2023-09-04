#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go


def create_gdf(geo_add, path_intersport):

    gdf = gpd.GeoDataFrame(geo_add,
                           geometry=gpd.points_from_xy(geo_add.longitude, geo_add.latitude),
                           crs="EPSG:4326")

    gdf.to_crs(epsg=2154, inplace=True)

    geo_intersport = pd.read_csv(path_intersport, sep=';')
    geo_intersport = gpd.GeoDataFrame(geo_intersport,
                                      geometry=gpd.points_from_xy(geo_intersport.longitude, geo_intersport.latitude),
                                      )

    geo_intersport.to_crs(epsg=2154, inplace=True)

    gdf_f = gpd.read_file('fr-poly.json')
    gdf_f.to_crs(epsg=2154, inplace=True)

    return geo_intersport, gdf


def create_layer(geo_intersport, gdf_f):

    distance = [75000, 50000, 30000, 15000]
    nom = ['Intersport_75km', 'Intersport_50km', 'Intersport_30km', 'Intersport_15km']

    gdf_distance = pd.DataFrame()

    for d, n in zip(distance, nom):
        df_d = gpd.GeoDataFrame({"Nom": n,
                                 "geometry": (geo_intersport.buffer(d))})
        df_d = df_d.overlay(gdf_f, how='intersection')
        if d == distance[0]:
            gdf_distance = gpd.GeoDataFrame(pd.concat([gdf_distance, df_d], ignore_index=True))
        else:
            gdf_distance.iloc[-1:] = gdf_distance.iloc[-1:].overlay(df_d, how='difference')
            gdf_distance = gpd.GeoDataFrame(pd.concat([gdf_distance, df_d], ignore_index=True))

    return gdf_distance


def gdf_join_groupby(gdf_distance, gdf):

    gdf_distance = gdf_distance.sjoin(gdf[['Utilise', 'geometry']],
                                      how='left',
                                      predicate="intersects")

    gdf_dist = gdf_distance[['Nom',
                             'Utilise',
                             'geometry']].dissolve(by='Nom',
                                                   aggfunc={"Utilise": [(lambda x:round((sum(x)/len(x)), 2)*100),
                                                                        'count']})

    gdf_dist = gdf_dist.rename(columns={('Utilise', '<lambda_0>'): 'Tx utilisation(%)',
                                        ('Utilise', 'count'): 'Nombre'
                                        })

    gdf_dist.reset_index()

    return gdf_dist


def choropleth_map(gdf_dist, geo_intersport):

    gdf_dist.to_crs(epsg=4326, inplace=True)
    geo_intersport.to_crs(epsg=4326, inplace=True)

    fig = px.choropleth_mapbox(data_frame=gdf_dist,
                               geojson=gdf_dist.geometry,
                               locations=gdf_dist.index,
                               color='Tx utilisation(%)',
                               range_color=(0, 100),
                               center={"lat": 47.7493897, "lon": -3.3977793},
                               mapbox_style='open-street-map',
                               color_continuous_scale='rdylgn',
                               opacity=0.75,
                               zoom=7,
                               hover_data={"Nombre": True},
                               hover_name=gdf_dist.index
                               )

    fig.update_traces(marker_line_width=1,
                      marker_opacity=0.8,
                      marker_line=dict(color="White")
                      )

    fig.add_scattermapbox(lat=geo_intersport.geometry.y,
                          lon=geo_intersport.geometry.x,
                          mode='markers',
                          marker=go.scattermapbox.Marker(
                             size=10, color='blue'),
                          text='Intersport',
                          hoverinfo='text'
                          )

    fig.update_geos(fitbounds='locations',
                    visible=False
                    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()

    fig.write_html("Bon_ratio_distance.html")

def analyse_geo_distance(geo_add, path_intersport, path_France):

    gdf_f = gpd.read_file(path_France)
    gdf_f.to_crs(epsg=2154, inplace=True)

    geo_intersport, gdf = create_gdf(geo_add, path_intersport)

    gdf_distance = create_layer(geo_intersport, gdf_f)

    gdf_dist = gdf_join_groupby(gdf_distance, gdf)

    choropleth_map(gdf_dist, geo_intersport)


if __name__ == '__main__':
    pass