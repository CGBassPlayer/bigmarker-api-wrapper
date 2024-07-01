from bigmarker.clients import ConferenceClient, AttendeeClient, RegistrationClient


class BigMarkerClient(ConferenceClient, AttendeeClient, RegistrationClient):
    pass
