from geo.geo import get_country_geometry
from api.datasets import get_dataset
import pandas as pd


query_dict = {'umd_tree_cover_gain':
              "SELECT mapbox_river_basins__id, sum(gfw_peatlands__Mg_CO2_ha) as gfw_peatlands__Mg_CO2_ha "
              "FROM results "
              "group by mapbox_river_basins__id",
              'umd_tree_cover_loss_from_fires':
              "SELECT mapbox_river_basins__id, "
              "rspo_southeast_asia_land_cover_2010__class, "
              "sum(gfw_peatlands__Mg_CO2_ha) as gfw_peatlands__Mg_CO2_ha,"
              "sum(gfw_deadwood_carbon__Mg_CO2_ha) as gfw_deadwood_carbon__Mg_CO2_ha,"
              "sum(gfw_litter_carbon__Mg_CO2_ha) as gfw_litter_carbon__Mg_CO2_ha "
              "FROM results "
              "group by mapbox_river_basins__id, "
              "rspo_southeast_asia_land_cover_2010__class",
              'gfw_forest_carbon_gross_emissions':
              "SELECT gfw_plantations__type, "
              # "mapbox_river_basins__id, "
              # "inpe_prodes__year, "
              "sum(esa_land_cover_2015__uint16) as esa_land_cover "
              # "sum(gfw_forest_carbon_gross_emissions__Mg_CO2e_px-1) as gfw_forest_carbon_gross_emissions, "
              # "sum(gfw_forest_carbon_gross_removals__Mg_CO2e_px) AS gfw_forest_carbon_gross_removals "
              "FROM results "
              "group by gfw_plantations__type "
              # "mapbox_river_basins__id, "
              # "inpe_prodes__year"
              }


def collect_data_for_country(country, dataset, version):
    """
        Queries the GFW API using the query from the dictionary in query.py
        and resolves the geo coordinates from the country you input
    """
    geometry = get_country_geometry(country)

    df = get_dataset(dataset=dataset,
                     version=version,
                     geometry=geometry,
                     query=query_dict[dataset])

    return df


def collect_country_data(country_list, dataset, version):
    """
        Queries the GFW API using the query from the dictionary in query.py
        and resolves the geo coordinates from the country list you input
    """
    df = pd.DataFrame()

    for country in country_list:

        df_import = collect_data_for_country(country=country,
                                             dataset=dataset,
                                             version=version)
        df_import['country'] = country

        df = pd.concat([df, df_import], ignore_index=True)

        del df_import

    return df

