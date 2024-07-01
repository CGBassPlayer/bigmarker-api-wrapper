import requests


class BaseClient:
    def __init__(self, token: str):
        self._session = requests.session()
        self._headers = {
            'API-KEY': token
        }
