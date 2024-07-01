from datetime import datetime
from typing import Optional, Literal

import requests
from pydantic import NonNegativeInt

from base import BaseClient
from bigmarker.models.conference import Conference, ConferencePresenter


class ConferenceClient(BaseClient):
    def _conferences(self, start_time: NonNegativeInt = 0):
        params: dict = {
            'type': 'all',
            'start_time': start_time
        }
        url = "https://www.bigmarker.com/api/v1/conferences"
        first_page = self._session.get(url, headers=self._headers, params=params).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            next_page = self._session.get(url, params=params | {'page': page}).json()
            yield next_page

    def _conferences_search(self, search_params: dict):
        params: dict = {
            'type': 'all',
        }
        url = f"https://www.bigmarker.com/api/v1/conferences/search/"
        first_page = self._session.get(url, headers=self._headers, params=params,
                                       data={k: v for k, v in search_params.items() if v is not None}).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            next_page = self._session.get(url, params=params | {'page': page}, data=search_params).json()
            yield next_page

    def get_all_conferences(self) -> list[Conference]:
        return [Conference(**c) for c in self._conferences()]

    def get_conferences_from_timeframe(self, start_time: datetime):
        return [Conference(**c) for c in self._conferences(start_time.timestamp())]

    def get_conference(self, conference_id: str) -> Optional[Conference]:
        res = requests.get(f"https://www.bigmarker.com/api/v1/conferences/{conference_id}",
                           headers=self._headers)
        if res.status_code != 200:
            return None
        return Conference(**res.json())

    def search_conference(self,
                          title: Optional[str] = None,
                          start_time: Optional[Conference.start_time] = None,
                          end_time: Optional[Conference.end_time] = None,
                          conference_ids: Optional[list[Conference.id]] = None,
                          presenter_member_ids: Optional[ConferencePresenter.presenter_id] = None,
                          role: Optional[Literal['hosting', 'attending', 'all']] = None) -> Optional[list[Conference]]:
        all_serach_params: dict = {
            'title': title,
            'start_time': start_time,
            'end_time': end_time,
            'conference_ids': ",".join(conference_ids) if conference_ids else None,
            'presenter_ids': ",".join(presenter_member_ids) if presenter_member_ids else None,
            'role': role
        }
        search_parameters: dict = {k: v for k, v in all_serach_params.items() if v is not None}
        return [Conference(**c) for c in self._conferences_search(search_parameters)]
