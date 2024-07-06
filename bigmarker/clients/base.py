from typing import Optional

import requests
from pydantic import EmailStr

from bigmarker.error.token import IncompleteLoginSetupException


class BaseClient:
    def __init__(self, token: Optional[str] = None, email: Optional[EmailStr] = None, password: Optional[str] = None):
        self._session = requests.session()
        if token is not None:
            self._headers = {
                'API-KEY': token
            }
        elif email and password is not None:
            res = self._session.get(url="https://www.bigmarker.com/api/v1/members/login",
                                    data=f"email={email}&password={password}")
            if res.status_code != 200:
                raise IncompleteLoginSetupException(f"Response from logging into BigMarker: {res.text}")
            self._headers = res.json()
        else:
            raise IncompleteLoginSetupException("API token or username and password must be provided")

    def _pages(self, url: str):
        first_page = self._session.get(url, headers=self._headers).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            next_page = self._session.get(url, params={'page': page}).json()
            yield next_page