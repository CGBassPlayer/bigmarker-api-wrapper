from typing import Optional

from .base import BaseClient
from bigmarker.models.attendees import Attendee


class AttendeeClient(BaseClient):
    def _attendees(self, conference_id: str):
        return self._pages(f"https://www.bigmarker.com/api/v1/{conference_id}/attendees/")

    def get_attendees(self, conference_id: str) -> Optional[list[Attendee]]:
        return [Attendee(**a) for a in self._attendees(conference_id)]
