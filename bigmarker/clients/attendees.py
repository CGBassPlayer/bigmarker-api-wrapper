from typing import Optional

from base import BaseClient
from bigmarker.models.attendees import Attendee
from bigmarker.models.conference import Conference


class AttendeeClient(BaseClient):
    def _attendees(self, conference_id: Conference.id):
        url = f"https://www.bigmarker.com/api/v1/{conference_id}/attendees/"
        first_page = self._session.get(url, headers=self._headers).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            next_page = self._session.get(url, params={'page': page}).json()
            yield next_page

    def get_attendees(self, conference_id: Conference.id) -> Optional[list[Attendee]]:
        return [Attendee(**a) for a in self._attendees(conference_id)]
