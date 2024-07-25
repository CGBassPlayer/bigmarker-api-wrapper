from datetime import datetime
from typing import Optional, Literal, Any

from pydantic import BaseModel, HttpUrl, EmailStr, NonNegativeInt, field_validator, field_serializer
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
    time_zone: Literal[
        "International Date Line West",
        "Midway Island",
        "American Samoa",
        "Hawaii",
        "Alaska",
        "Pacific Time (US & Canada)",
        "Tijuana",
        "Mountain Time (US & Canada)",
        "Arizona",
        "Chihuahua",
        "Mazatlan",
        "Central Time (US & Canada)",
        "Saskatchewan",
        "Guadalajara",
        "Mexico City",
        "Monterrey",
        "Central America",
        "Eastern Time (US & Canada)",
        "Indiana (East)",
        "Bogota",
        "Lima",
        "Quito",
        "Atlantic Time (Canada)",
        "Caracas",
        "La Paz",
        "Santiago",
        "Newfoundland",
        "Brasilia",
        "Buenos Aires",
        "Georgetown",
        "Greenland",
        "Mid-Atlantic",
        "Azores",
        "Cape Verde Is.",
        "Dublin",
        "Edinburgh",
        "Lisbon",
        "London",
        "Casablanca",
        "Monrovia",
        "UTC",
        "Belgrade",
        "Bratislava",
        "Budapest",
        "Ljubljana",
        "Prague",
        "Sarajevo",
        "Skopje",
        "Warsaw",
        "Zagreb",
        "Brussels",
        "Copenhagen",
        "Madrid",
        "Paris",
        "Amsterdam",
        "Berlin",
        "Bern",
        "Rome",
        "Stockholm",
        "Vienna",
        "West Central Africa",
        "Bucharest",
        "Cairo",
        "Helsinki",
        "Kyiv",
        "Riga",
        "Sofia",
        "Tallinn",
        "Vilnius",
        "Athens",
        "Istanbul",
        "Minsk",
        "Jerusalem",
        "Harare",
        "Pretoria",
        "Moscow",
        "St. Petersburg",
        "Volgograd",
        "Kuwait",
        "Riyadh",
        "Nairobi",
        "Baghdad",
        "Tehran",
        "Abu Dhabi",
        "Muscat",
        "Baku",
        "Tbilisi",
        "Yerevan",
        "Kabul",
        "Ekaterinburg",
        "Islamabad",
        "Karachi",
        "Tashkent",
        "Chennai",
        "Kolkata",
        "Mumbai",
        "New Delhi",
        "Kathmandu",
        "Astana",
        "Dhaka",
        "Sri Jayawardenepura",
        "Almaty",
        "Novosibirsk",
        "Rangoon",
        "Bangkok",
        "Hanoi",
        "Jakarta",
        "Krasnoyarsk",
        "Beijing",
        "Chongqing",
        "Hong Kong",
        "Urumqi",
        "Kuala Lumpur",
        "Singapore",
        "Taipei",
        "Perth",
        "Irkutsk",
        "Ulaan Bataar",
        "Seoul",
        "Osaka",
        "Sapporo",
        "Tokyo",
        "Yakutsk",
        "Darwin",
        "Adelaide",
        "Canberra",
        "Melbourne",
        "Sydney",
        "Brisbane",
        "Hobart",
        "Vladivostok",
        "Guam",
        "Port Moresby",
        "Magadan",
        "Solomon Is.",
        "New Caledonia",
        "Fiji",
        "Kamchatka",
        "Marshall Is.",
        "Auckland",
        "Wellington",
        "Nuku'alofa",
        "Tokelau Is.",
        "Samoa"]
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


class ConferenceCreate(BaseModel):
    channel_id: str
    title: str
    conference_copy_id: Optional[str] = None
    presenter_exit_url: Optional[HttpUrl] = None
    sub_url: Optional[HttpUrl] = None
    enable_dial_in: Optional[bool] = None
    purpose: Optional[str] = None
    time_zone: Optional[Literal[
        "International Date Line West",
        "Midway Island",
        "American Samoa",
        "Hawaii",
        "Alaska",
        "Pacific Time (US & Canada)",
        "Tijuana",
        "Mountain Time (US & Canada)",
        "Arizona",
        "Chihuahua",
        "Mazatlan",
        "Central Time (US & Canada)",
        "Saskatchewan",
        "Guadalajara",
        "Mexico City",
        "Monterrey",
        "Central America",
        "Eastern Time (US & Canada)",
        "Indiana (East)",
        "Bogota",
        "Lima",
        "Quito",
        "Atlantic Time (Canada)",
        "Caracas",
        "La Paz",
        "Santiago",
        "Newfoundland",
        "Brasilia",
        "Buenos Aires",
        "Georgetown",
        "Greenland",
        "Mid-Atlantic",
        "Azores",
        "Cape Verde Is.",
        "Dublin",
        "Edinburgh",
        "Lisbon",
        "London",
        "Casablanca",
        "Monrovia",
        "UTC",
        "Belgrade",
        "Bratislava",
        "Budapest",
        "Ljubljana",
        "Prague",
        "Sarajevo",
        "Skopje",
        "Warsaw",
        "Zagreb",
        "Brussels",
        "Copenhagen",
        "Madrid",
        "Paris",
        "Amsterdam",
        "Berlin",
        "Bern",
        "Rome",
        "Stockholm",
        "Vienna",
        "West Central Africa",
        "Bucharest",
        "Cairo",
        "Helsinki",
        "Kyiv",
        "Riga",
        "Sofia",
        "Tallinn",
        "Vilnius",
        "Athens",
        "Istanbul",
        "Minsk",
        "Jerusalem",
        "Harare",
        "Pretoria",
        "Moscow",
        "St. Petersburg",
        "Volgograd",
        "Kuwait",
        "Riyadh",
        "Nairobi",
        "Baghdad",
        "Tehran",
        "Abu Dhabi",
        "Muscat",
        "Baku",
        "Tbilisi",
        "Yerevan",
        "Kabul",
        "Ekaterinburg",
        "Islamabad",
        "Karachi",
        "Tashkent",
        "Chennai",
        "Kolkata",
        "Mumbai",
        "New Delhi",
        "Kathmandu",
        "Astana",
        "Dhaka",
        "Sri Jayawardenepura",
        "Almaty",
        "Novosibirsk",
        "Rangoon",
        "Bangkok",
        "Hanoi",
        "Jakarta",
        "Krasnoyarsk",
        "Beijing",
        "Chongqing",
        "Hong Kong",
        "Urumqi",
        "Kuala Lumpur",
        "Singapore",
        "Taipei",
        "Perth",
        "Irkutsk",
        "Ulaan Bataar",
        "Seoul",
        "Osaka",
        "Sapporo",
        "Tokyo",
        "Yakutsk",
        "Darwin",
        "Adelaide",
        "Canberra",
        "Melbourne",
        "Sydney",
        "Brisbane",
        "Hobart",
        "Vladivostok",
        "Guam",
        "Port Moresby",
        "Magadan",
        "Solomon Is.",
        "New Caledonia",
        "Fiji",
        "Kamchatka",
        "Marshall Is.",
        "Auckland",
        "Wellington",
        "Nuku'alofa",
        "Tokelau Is.",
        "Samoa"]] = None
    room_logo: Optional[HttpUrl] = None
    conference_logo: Optional[HttpUrl] = None
    apply_conference_logo_to_channel: Optional[bool] = None
    room_sub_title: Optional[str] = None
    schedule_type: Optional[Literal["24_hour_room", "one_time"]] = None
    start_time: datetime = None
    recurring_start_times: list[datetime] = None
    webcast_mode: Optional[Literal["automatic", "required", "optional"]] = None
    duration_minutes: Optional[int] = None
    who_can_watch_recording: Optional[
        Literal["everyone", "channel_admin_only", "channel_subscribers", "attendees", "attendees_registrants"]] = None
    presenter_advanced_enter_time: Optional[Literal["60", "120", "180"]] = None
    attendee_advanced_enter_time: Optional[Literal["15", "30"]] = None
    privacy: Optional[Literal["private", "public"]] = None
    webinar_format: Optional[Literal["webinar", "livestream", "on_demand"]] = None
    ondemand_video_url: Optional[HttpUrl] = None
    enable_knock_to_enter: Optional[bool] = None
    registration_conf_emails: Optional[bool] = None
    send_notification_emails_to_presenters: Optional[bool] = None
    send_reminder_emails_to_presenters: Optional[bool] = None
    show_reviews: Optional[bool] = None
    review_emails: Optional[bool] = None
    poll_results: Optional[bool] = None
    enable_ie_safari: Optional[bool] = None
    enable_twitter: Optional[bool] = None
    send_cancellation_email: Optional[bool] = None
    webhook_url: Optional[HttpUrl] = None
    exit_url: Optional[HttpUrl] = None
    enable_create_webinar_reg_webhook: Optional[bool] = None
    enable_new_reg_webhook: Optional[bool] = None
    new_reg_webhook_url: Optional[HttpUrl] = None
    enable_webinar_start_webhook: Optional[bool] = None
    webinar_start_webhook_url: Optional[HttpUrl] = None
    enable_waiting_room_open_webhook: Optional[bool] = None
    waiting_room_open_webhook_url: Optional[HttpUrl] = None
    enable_webinar_end_webhook: Optional[bool] = None
    webinar_end_webhook_url: Optional[HttpUrl] = None
    enable_live_attendee_data_webhook: Optional[bool] = None
    live_attendee_data_webhook_url: Optional[HttpUrl] = None
    enable_on_demand_viewer_webhook: Optional[bool] = None
    on_demand_viewer_webhook_url: Optional[HttpUrl] = None
    registration_required_to_view_recording: Optional[bool] = None
    channel_admin_id: Optional[str] = None
    background_image_url: Optional[HttpUrl] = None
    room_type: Optional[Literal["1", "attendee_as_presenter", "attendee_mic_and_cam"]] = None
    display_language: Optional[str] = None
    show_handout_on_page: Optional[bool] = None
    banner_filter_percentage: Optional[int] = None
    icon: Optional[HttpUrl] = None
    webinar_tags: Optional[dict[str, str]] = None

    model_config = {
        "extra": "ignore",
        "str_strip_whitespace": True
    }

    @field_validator("duration_minutes")
    def validate_duration_minutes(self, value: int):
        if 1 <= value <= 720:
            return value
        raise ValueError("duration_minutes must be between 1 and 720")

    @field_validator("banner_filter_percentage")
    def validate_banner_filter_percentage(self, value: int):
        if 0 <= value <= 0.6:
            return value
        return ValueError("banner_filter_percentage must be between 0 and 0.6")

    @field_serializer("duration_minutes", "banner_filter_percentage", when_used="json")
    def convert_to_str(self, value: Any) -> str:
        return str(value)


class FileStatus(BaseModel):
    success: bool
    message: str


class UploadFileStatus(FileStatus):
    id: Optional[str] = None
    type: Optional[str] = None


class HandoutUpload(BaseModel):
    title: str
    handout_link: HttpUrl
    handout_ull: HttpUrl


class HandoutItem(HandoutUpload):
    icon_url: Optional[HttpUrl] = None
