import requests
from pydantic import HttpUrl

from .base import BaseClient
from bigmarker.models.registrations import Registration, UserRegistrant, Registered


class RegistrationClient(BaseClient):
    def _registrations(self, conference_id: str, keyword: str = "registrations"):
        return self._pages(f"https://www.bigmarker.com/api/v1/conferences/{keyword}/{conference_id}")

    def get_registration(self, registration_id: str) -> Registration:
        pass

    def get_registrations(self, conference_id: str) -> list[Registration]:
        return [Registration(**r) for r in self._registrations(conference_id)]

    def get_checked_in_registrations(self, conference_id: str) -> list[Registration]:
        return [Registration(**r) for r in self._registrations(conference_id, "checked_in_registrations")]

    def register_user(self, registrant: UserRegistrant) -> HttpUrl | str:
        response = requests.put(url=f"https://www.bigmarker.com/api/v1/conferences/register",
                                headers=self._headers,
                                json=registrant.model_dump_json(by_alias=True,
                                                                exclude_none=True))
        if response.status_code == 401:
            return "You do not have permission to access or modify this conference."
        elif response.status_code == 404:
            return "The conference you are requesting is not found."

        return response.json()["conference_url"]
