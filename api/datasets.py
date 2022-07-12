import requests
import json
import sys
import random
import pandas as pd
sys.path.append('api/..')
import api.config as config
from api.api_token import get_api_token


def update_datasets_json():
    """
        Takes the variables stored in api/config.py and creates a POST request to the API.
        Information including the token required to access data from the provider is returned.
        This will be ran if this script is called directly - see below for __main__
    """
    token = get_api_token()

    headers = {'x-api-key': token}

    api_reply = requests.get(url=config.url_datasets, headers=headers)

    datasets = api_reply.text

    datasets = json.loads(datasets)

    with open('api/datasets.json', 'w', encoding='utf-8') as f:
        json.dump(datasets, f, ensure_ascii=False, indent=4)

        print('SUCCESS: api/datasets.json updated')


def keyword_search(keyword):
    """
        Performs a simple keyword search against the list of datasets and returns those which include that keyword
    """

    datasets = list_dataset_names()

    matching_datasets = [d for d in datasets if keyword in d]

    if not matching_datasets:
        print(f'No datasets found for keyword {keyword}')

    return matching_datasets


def get_dataset_fields(dataset, version):
    """
        Takes the variables stored in api/config.py and creates a POST request to the API.
        Information including the token required to access data from the provider is returned.
    """
    token = get_api_token()

    headers = {'x-api-key': token}

    url = f'{config.url_dataset}/{dataset}/{version}/fields'

    api_reply = requests.get(url=url, headers=headers)

    fields = api_reply.text

    return fields


def get_dataset_detail(dataset, attributes=False):
    """
        Returns the detail including version history etc for a specific dataset
    """

    with open('api/datasets.json') as f:
        datasets_json = json.load(f)

    datasets = datasets_json['data']

    detail = [d for d in datasets if d['dataset'] == dataset]

    if not attributes:
        return detail
    else:
        return dict((k, detail[0][k]) for k in attributes if k in detail[0])


def get_dataset(dataset, version, geometry, query):
    """
        Returns the dataset
    """
    token = get_api_token()

    headers = {'Authorization': token,
               'Content_Type': 'application/json'}

    data = {"geometry": geometry,
            "sql": query
            }

    data = json.dumps(data)

    url = f'{config.url_dataset}/{dataset}/{version}/query'

    response = requests.post(url=url, headers=headers, data=data)

    dataset = json.loads(response.content)

    dataset_data = json.dumps(dataset['data'])

    df = pd.read_json(dataset_data)

    return df


def list_dataset_names():
    """
        Creates simple list of data sets from the datasets json
    """
    lst = []

    with open('api/datasets.json') as f:
        datasets = json.load(f)

    for item, dataset in enumerate(datasets['data']):
        lst.append(dataset['dataset'])

    return lst


def list_random_n_datasets(n):
    """
        Takes n and returns random dataset names as a list
    """

    datasets = list_dataset_names()

    return random.sample(datasets, n)


if __name__ == "__main__":

    update_datasets_json()
