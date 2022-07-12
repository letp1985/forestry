import requests
import json
import sys
sys.path.append('api/..')
from api.config import url_token, headers, data


def get_access_token():
    """
        Takes the variables stored in api/config.py and creates a POST request to the API.
        Information including the token required to access data from the provider is returned.
    """

    api_reply = requests.post(url=url_token,
                              headers=headers,
                              data=data)

    return api_reply.text


def update_api_token():

    """
        Stores the API token locally in api_token.json
    """
    access_token = json.loads(get_access_token())

    with open('api/api_token.json', 'w', encoding='utf-8') as f:

        json.dump(access_token, f, ensure_ascii=False, indent=4)

        print('api_token_updated')


def get_api_token():
    """
        Retrieve API from json file
    """
    with open('api_token.json') as f:
        api_info = json.load(f)

    api_token = api_info['data']['access_token']

    return api_token


if __name__ == '__main__':

    update_api_token()

