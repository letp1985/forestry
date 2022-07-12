import geopandas as gpd
import geojson


def get_country_geometry(country_name):
    """
        Uses GEO Pandas and geojason to convert the response from geo polygon string to geo jason
    """
    # todo error handling for wrong country name

    # available = gpd.datasets.available
    # print(available)

    path_data = gpd.datasets.get_path("naturalearth_lowres")
    df_data = gpd.read_file(path_data)
    df_data_item = df_data[df_data.name == country_name][['name', 'geometry']]
    geo = df_data_item.iloc[0]['geometry']
    geo_json = geojson.Feature(geometry=geo, properties={})

    geometry = geo_json.geometry

    return geometry

# example for NY boroughs
# path_data = gpd.datasets.get_path("nybb")
# df_data = gpd.read_file(path_data)
# df_data_item = df_data[df_data.BoroName == 'Manhattan'][['BoroName', 'geometry']]
# print(df_data_item)

