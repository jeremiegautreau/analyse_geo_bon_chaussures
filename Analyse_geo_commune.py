import pandas as pd
import geopandas as gpd
import plotly.express as px
from shapely.validation import make_valid


def analyse_geo_com(geo_add, path_com):

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

    # gdf_com.head()

    gdf_ratio_com = pd.merge(gdf_ratio,
                             gdf_com[['codgeo', 'geometry']],
                             left_on='result_citycode',
                             right_on='codgeo',
                             how='left'
                             )


    gdf_ratio_com = gpd.GeoDataFrame(gdf_ratio_com, crs="EPSG:4326")

    # gdf_ratio_com = gdf_ratio_com.set_crs(epsg=3857,
    #                                     allow_override=True,
    #                                     inplace=True
    #                                     )

    # gdf_ratio_com.to_crs(epsg=3857, inplace=True)

    gdf_ratio_com = gdf_ratio_com.iloc[:, [4, 0, 1, 2, 3]]  # nécessaire?


    gdf_ratio_com = gpd.GeoDataFrame(gdf_ratio_com)
    gdf_ratio_com['validite'] = gdf_ratio_com.geometry.is_valid
    gdf_ratio_com.geometry.dropna(inplace=True)
    gdf_ratio_com = gdf_ratio_com.drop(index='Paris')
    gdf_ratio_com.geometry = gdf_ratio_com.apply(lambda row: make_valid(row.geometry) if not row.geometry.is_valid else row.geometry, axis=1)

    gdf_ratio_com = gdf_ratio_com.set_index("result_city")

    fig = px.choropleth_mapbox(data_frame=gdf_ratio_com,
                               geojson=gdf_ratio_com.geometry,
                               locations=gdf_ratio_com.index,
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
                               hover_name=gdf_ratio_com.index)

    fig.update_traces(marker_line_width=1, marker_opacity=0.8, marker_line=dict(color="White"))
    fig.update_geos(fitbounds='locations',
                    visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()

    fig.write_html("Bon_ratio_com.html")
