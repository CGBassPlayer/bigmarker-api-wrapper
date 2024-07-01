from pydantic import BaseModel


class Attendee(BaseModel):
    id: str
    conference_id: str
