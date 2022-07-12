# forestry

An example project using Python to interface with data
from Global Forest Watch (GFW) API.

https://data.globalforestwatch.org/

## Goal

The goal of this project is to support a researcher who wishes to use python to extract and transform data from the 
Global Forest Watch resource. 

The researcher has a limited knowledge of python and no experience accessing APIs.

They have requested a pre built template with working examples 
of how to achieve the following items:

- Query the API and return a token which allows them to connect to Global Forest Watch datasets 
- Find all available datasets
- View metadata for datasets including versions, geographic coverage etc
- Automatically gather geo coordinates (e.g polygon) for given inputs (i.e. a list of countries)
- Build custom queries against specific datasets based on the coordinates 
- Get the data from the GFW into a pandas dataframe for them to start analysing.

## Pre requisites

First make sure that all requirements for this project are fulfilled in your environment (e.g venv)

```
$ pip install -r requirements.txt
```

In order to use the GFW API, users must create an account with GFW (https://globalforestwatch.org/) 

The file `/api/config.py` needs to be created manually as this is included in `.gitignore`

Create the file and include the content below, including your `username` and `password` for GFW.

```
# Connection to Global Forest Watch
# See documentation here: https://www.globalforestwatch.org/help/developers/guides/create-and-use-an-api-key/

url_prefix = 'https://data-api.globalforestwatch.org/'
# for getting a token
url_token = f'{url_prefix}auth/token'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# for accessing datasets information
url_datasets = f'{url_prefix}datasets'
# for accessing dataset information
url_dataset = f'{url_prefix}dataset'

# user info
data = {'username': 'INSERT USER NAME HERE',
        'password': 'INSERT PASSWORD HERE'}
```

Please update the `username` and `password` accordingly.


To retrieve your API token, run the following Terminal command 
from the api root directory

```
python api/api_token.py 
```

Your token will be updated and saved in a file called `api/api_token.json`

This is also included in the .gitignore file


Before starting, please make sure the `api/..` folder is in your sys.path.
 
```
import sys
sys.path.append('api/..')
```
Read more about why here: https://www.geeksforgeeks.org/sys-path-in-python/

You will also see this statement included in the *.py files you call below.


#### End of setup

You are now ready to start interacting with the api.


### Example functions


Run the below in the terminal (from the project root directory)


```
python api/datasets.py
```

This automatically calls the function `update_datasets_json()` 
from `api/datasets.py` and the file `api/datasets.json` will be updated 
with the latest datasets.

Now switch to the python console.

If you would like to list all the datasets, run the following. 

```
from api.datasets import list_dataset_names

datasets = list_dataset_names()
print(datasets)
```

This returns a list of datasets by parsing the `api\datasets.json` 
and returning the dataset element for each entry.

As the list is long, you can use the following function to list 5 random datasets.
```
from api.datasets import list_random_n_datasets

n = 5

datasets = list_random_n_datasets(n)
print(datasets)
```

Perhaps you want to search for a keyword in the dataset name?

In the example below we return all datasets with the word **tree** 


```
from api.datasets import keyword_search

keyword = 'tree'

datasets = keyword_search(keyword)
print(datasets)
```

Once you have found a dataset you are interested in, you need to know what fields
you can base your query on. 

The below function call will return all the dataset's field metadata 
(e.g. field_name, field_alias, field_description, field_values)
for the dataset **'umd_tree_cover_gain'**.

We can also pass in a specific version. Here we choose 'latest'

```
from api.datasets import get_dataset_fields

dataset = 'umd_tree_cover_gain'
version = 'latest'

fields = get_dataset_fields(dataset,version)
print(fields)

```

The Global Forestry Watch only accept queries against datasets by passing in geo coordinate parameters.

This must be a GeoJSON formatted geometry. 

Visit https://geojson.io to easily create a GeoJSON formatted geometry on the map.

Read the documentation here: https://www.globalforestwatch.org/help/developers/guides/query-data-for-a-custom-geometry/

This forestry project also includes access to the libraries `geopandas` and `geojson` to
help you access coordinates in a fast way.

For example, you may want to quickly get the geo coordinates for a given country
and be confident it is in the right format when accessing the API.

In the script geo/geo.py you can see how this example function has been built.

Here is an example of how to call it and return the coordinates for the Netherlands in GeoJson 

```
from geo.geo import get_country_geometry

country = 'Netherlands'

geo = get_country_geometry(country)
print(geo)

```

You are now in a position to build your query and return a dataset in the format of a pandas dataframe.

The query input with your chosen field names and criteria must be in SQL.

It is useful for users of this project to have experience building simple SQL queries.

In `query.py` the dictionary `query_dict` has been setup to allow you to input 
a key of dataset name, and a value of a pre built SQL statement. This might be 
very helpful if running the same query for multiple countries, but it a little ugly so feel free 
to find a solution that works for you. There are some example already created inside this dictionary.

In `query.py` the main function `collect_country_data()` returns a dataset 
for multiple countries at the same time by providing a list of countries.
Each country from this list is then passed into the API with your query.
 
Each countries results are then concatenated into one pandas dataframe.

In our first example we use the country list and dataset below along with the 
prebuilt SQL statement in the `query_dict` in `query.py` which returns a number of CO2 related
measures by country and southeast_asia_land_cover_2010__class.  

```
from api.query import collect_country_data

country_list = ['Thailand', 'Indonesia']
dataset = 'umd_tree_cover_loss_from_fires'
version = 'latest'

df = collect_country_data(country_list, dataset, version)

print(df)

```
In our second example we use a new country list and different dataset.

This query focuses on the measure gfw_peatlands__Mg_CO2 by mapbox_river_basins__id and country.

```
from api.query import collect_country_data

country_list = ['France', 'Spain', 'Netherlands', 'Germany']
dataset = 'umd_tree_cover_gain'
version = 'latest'

df = collect_country_data(country_list, dataset, version)

print(df)

```

Some simple pandas functions are below to get you started.

```
# simple statistics regarding the dataset
df.describe()

# Count the instances of each country in this dataset
df.country.value_counts()

# Group the country and sum the gfw_peatlands__Mg_CO2_ha measure
df.groupby(['country'])['gfw_peatlands__Mg_CO2_ha'].sum()

```


By using these examples and adapting the functions throughout this project,
you are now able to query the GFW API and return a pandas dataframe with your data. 

Pandas is  a very useful tool for working with structured datasets, especially when integrating
numpy.

Check the documentation/links below

https://pandas.pydata.org/

https://numpy.org/

## Supporting material

Global Forest Watch Developer Guide

https://www.globalforestwatch.org/help/developers/guides/



