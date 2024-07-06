from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class Registered(str, Enum):
    registered = 'registered'


class Registration(BaseModel):
    email: str
    first_name: str
    last_name: str
    enter_url: HttpUrl
    bmid: str
    referral_domain: str
    source: str
    tracking_code: str
    earned_certificate: bool
    qualified_for_certificate: bool
    qr_code_value: str


class UserRegistrant(BaseModel):
    conference_id: str = Field(alias='id')
    first_name: str
    last_name: str
    temporary_password: Optional[str] = None
    custom_fields: Optional[dict[str, Any]] = None
    utm_bmcr_source: Optional[str] = None
    custom_user_id: Optional[str] = None
