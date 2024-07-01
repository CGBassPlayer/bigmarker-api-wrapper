from pydantic import BaseModel, EmailStr


class Attendee(BaseModel):
    id: str
    conference_id: str
    email: EmailStr
    first_name: str
    last_name: str
