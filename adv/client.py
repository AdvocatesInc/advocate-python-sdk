import os

import requests

from .exceptions import APIException
# from .dctas import DCTA
# from .widgets import Widget


class AdvocateClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = os.environ.get('ADVOCATE_API_URL', 'https://api.adv.gg/v1/')

        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        self.session.mount('https://', adapter)

        self.dctas = {}
        self.widgets = {

        }

    def _call_advocate_api(self, method, endpoint, data=None, params={}):
        """
        Low level manager for interfacing with the Advocate API.
        All requests to the API will be handled by this function
        """
        api_call = getattr(self.session, method)
        url = self.api_url + endpoint

        headers = {
            'Authorization': 'API-Key: {}'.format(self.api_key),
        }

        response = api_call(url, json=data, headers=headers)

        if response.status_code >= 200 and response.status_code < 300:
            return response.json() if response.content != b'' else ''
        elif response.status_code >= 400 and response.status_code < 500:
            raise APIException(response.json())
        else:
            raise APIException('Cannot connect to the Advocate API')

    def get(self, endpoint):
        """
        Make a `get` request to the Advocate API
        """
        return self._call_advocate_api(endpoint)

    def get_dctas(self):
        """
        Fetches and deserializes all DCTAs from the user's account
        """
        pass

    def get_dcta(self, dcta_id):
        """
        Fetchs and deserializes a signle DCTA from the user's account
        """
        pass
