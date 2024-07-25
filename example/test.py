from bigmarker import BigMarkerClient
from bigmarker.types import Conference, Attendee, Registration, UserRegistrant


def main():
    bm_client = BigMarkerClient(token="abc123")
    # bm_client = BigMarkerClient(email="test@test.com", password="test")

    conferences: list[Conference] = bm_client.get_all_conferences()

    for conference in conferences:
        print(conference.id)  # Code Editors understand that what values are available

    single_conference: Conference = bm_client.get_conference("hex3ghn0x")

    print(single_conference.model_dump_json())  # Pydantic Models give extra conversion features out of the box too

    search_results: list[Conference] = bm_client.search_conference(title="Test",
                                                                   conference_ids=[single_conference.id,
                                                                                   "1gfdstgf43343"])

    print([sr.model_dump_json(indent=2) for sr in search_results])

    conference_attendees: list[Attendee] = bm_client.get_attendees(single_conference.id)
    conference_registrations: list[Registration] = bm_client.get_registrations(single_conference.id)

    for attendee in conference_attendees:
        print(attendee.model_dump_json(indent=2))
    for registration in conference_registrations:
        print(registration.model_dump_json(indent=2))

    url = bm_client.register_user(UserRegistrant(
        conference_id=single_conference.id,
        first_name="Test",
        last_name="Test",
        temporary_password="<PASSWORD>",
        custom_fields={
            "eid": "abc#123",
            "test": True
        }
    ))

    created_conference = bm_client.create_conference(channel_id="principal",
                                                     title="test")


if __name__ == '__main__':
    main()
