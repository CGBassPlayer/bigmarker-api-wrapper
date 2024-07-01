from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, HttpUrl, EmailStr, NonNegativeInt
from pydantic_extra_types.phone_numbers import PhoneNumber


class ConferenceClosedCaptions(BaseModel):
    enable_closed_caption: bool
    cc_original_language: str
    cc_display_language: Optional[str]


class ConferenceDialInInformation(BaseModel):
    dial_in_number: PhoneNumber
    dial_in_id: Optional[str]
    dial_in_passcode: Optional[str]
    presenter_dial_in_number: PhoneNumber
    presenter_dial_in_id: Optional[str]
    presenter_dial_in_passcode: Optional[str]


class ConferencePreloadFile(BaseModel):
    id: str
    file_name: str
    file_type: str
    file_url: HttpUrl


class ConferencePresenter(BaseModel):
    presenter_id: str
    member_id: str
    conference_id: str
    display_name: str
    display_on_landing_page: bool
    first_name: str
    last_name: str
    email: EmailStr
    presenter_url: HttpUrl
    presenter_dial_in_number: PhoneNumber
    presenter_dial_in_id: str
    presenter_dial_in_passcode: str
    title: Optional[str]
    bio: Optional[str]
    can_manage: bool
    is_moderator: bool
    facebook: Optional[str]
    twitter: Optional[str]
    linkedin: Optional[str]
    website: Optional[str]


class ConferenceWebinarStats(BaseModel):
    registrants: NonNegativeInt
    revenue: str
    total_attendees: NonNegativeInt
    page_views: NonNegativeInt
    invited: NonNegativeInt


class Conference(BaseModel):
    id: str
    title: str
    event_type: str
    language: str
    meeting_mode: bool
    type: Literal[
        'evergreen_parent',
        'evergreen_child',
        'recurring_parent',
        'recurring_child',
        'meetingspace',
        'ondemand',
        'live_webinar',
        'webcast'
    ]
    copy_webinar_id: Optional[str]
    master_webinar_id: Optional[str]
    max_attendees: NonNegativeInt
    purpose: str
    start_time: datetime
    duration: NonNegativeInt
    conference_address: HttpUrl
    banner_filter_percentage: str
    custom_event_id: Optional[str]
    channel_id: str
    webcast_mode: str
    closed_captions: ConferenceClosedCaptions
    end_time: datetime
    moderator_open_time: datetime
    audience_open_time: datetime
    first_admin_enter_time: datetime
    manual_end_time: datetime
    dial_in_information: ConferenceDialInInformation
    time_zone: str
    privacy: str
    exit_url: Optional[HttpUrl]
    enable_registration_email: bool
    enable_knock_to_enter: bool
    send_reminder_emails_to_presenters: bool
    enable_review_emails: bool
    can_view_poll_results: bool
    enable_ie_safari: bool
    enable_twitter: bool
    auto_invite_all_channel_members: bool
    send_cancellation_email: bool
    show_reviews: bool
    recording_url: Optional[HttpUrl]
    registration_required_to_view_recording: bool
    recording_iframe: str
    who_can_watch_recording: str
    show_handout_on_page: bool
    background_image_url: Optional[HttpUrl]
    fb_open_graph_image_url: Optional[HttpUrl]
    agenda_topics: list[str]
    preload_files: list[ConferencePreloadFile]
    disclaimer: Optional[str]
    presenters: list[ConferencePresenter]
    recorded: bool
    webinar_stats: ConferenceWebinarStats
    associated_series: Optional[list[str]]
    tags: Optional[list[str]]

    model_config = {
        "str_strip_whitespace": True
    }
