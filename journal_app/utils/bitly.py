import json

from django.conf import settings

import requests


def shortener(link):
    api_link = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': f'Bearer {settings.BITLY_TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {
        "long_url": f'{link}',

    }
    response = requests.post(api_link, headers=headers, data=json.dumps(data))
    returned_data = json.loads(response.text)
    return returned_data['id']
