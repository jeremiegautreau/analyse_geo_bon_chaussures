import pandas as pd
import geopandas as gpd
import plotly.express as px
from shapely.validation import make_valid


def group_com(geo_add, path_com):

    gdf_ratio = pd.pivot_table(geo_add, values=['Utilise'],
                               index=['result_city', 'result_citycode'],
                               aggfunc={'Utilise': [lambda x:round((sum(x)/len(x)*100), 2), 'count']})

    gdf_ratio = gdf_ratio.droplevel(0, axis=1)
    gdf_ratio = gdf_ratio.reset_index()
    gdf_ratio = gdf_ratio.rename(columns={'<lambda_0>': 'ratio', 'count': 'Nombre'})

    gdf_ratio['result_citycode'] = gdf_ratio['result_citycode'].astype(int)
    gdf_ratio['result_citycode'] = gdf_ratio['result_citycode'].astype(str)
    gdf_ratio['result_city'] = gdf_ratio['result_city'].astype(str)

    gdf_com = gpd.read_file(path_com)

    gdf_ratio_com = pd.merge(gdf_ratio,
                             gdf_com[['codgeo', 'geometry']],
                             left_on='result_citycode',
                             right_on='codgeo',
                             how='left'
                             )

    gdf_ratio_com = gpd.GeoDataFrame(gdf_ratio_com, crs="EPSG:4326")

    gdf_ratio_com = gpd.GeoDataFrame(gdf_ratio_com)

    return gdf_ratio_com


def repair_clean_gdf(gdf):

    gdf['validite'] = gdf.geometry.is_valid
    gdf.geometry.dropna(inplace=True)
    gdf = gdf.drop(index='Paris')
    gdf.geometry = gdf.apply(lambda row: make_valid(row.geometry) if not row.geometry.is_valid else row.geometry, axis=1)

    return gdf


def choropleth_map(gdf):

    gdf = gdf.set_index("result_city")

    fig = px.choropleth_mapbox(data_frame=gdf,
                               geojson=gdf.geometry,
                               locations=gdf.index,
                               color="ratio",
                               center={"lat": 47.7493897, "lon": -3.3977793},
                               mapbox_style='open-street-map',
                               labels={'ratio': 'utilisation',
                                       'result_city': 'Commune',
                                       'Nombre': 'Nb'},
                               color_continuous_scale='rdylgn',
                               opacity=0.75,
                               zoom=7,
                               hover_data=['Nombre'],
                               hover_name=gdf.index)

    fig.update_traces(marker_line_width=1, marker_opacity=0.8, marker_line=dict(color="White"))
    fig.update_geos(fitbounds='locations',
                    visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()

    fig.write_html("Bon_ratio_com.html")


def analyse_geo_com(geo_add, path_com):

    gdf_ratio_com = group_com(geo_add, path_com)

    gdf_ratio_com = repair_clean_gdf(gdf_ratio_com)

    choropleth_map(gdf_ratio_com)


if __name__ == '__main__':
    pass
