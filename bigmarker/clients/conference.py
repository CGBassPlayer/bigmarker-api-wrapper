from datetime import datetime
from typing import Optional, Literal

import requests
from pydantic import NonNegativeInt, HttpUrl

from .base import BaseClient
from bigmarker.models.conference import Conference, ConferenceCreate, FileStatus, UploadFileStatus


class ConferenceClient(BaseClient):
    def _conferences(self,
                     url: HttpUrl = "https://www.bigmarker.com/api/v1/conferences",
                     start_time: NonNegativeInt = 0):
        params: dict = {
            'type': 'all',
            'start_time': start_time
        }
        url = url
        first_page = self._session.get(url,
                                       headers=self._headers,
                                       params=params).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            next_page = self._session.get(url,
                                          params=params | {'page': page}).json()
            yield next_page

    def _conferences_search(self, search_params: dict):
        params: dict = {
            'type': 'all',
        }
        url = f"https://www.bigmarker.com/api/v1/conferences/search/"
        first_page = self._session.get(url,
                                       headers=self._headers,
                                       params=params,
                                       data={k: v for k, v in search_params.items() if v is not None}).json()
        yield first_page
        num_pages = first_page['total_pages']

        for page in range(2, num_pages + 1):
            next_page = self._session.get(url,
                                          params=params | {'page': page},
                                          data=search_params).json()
            yield next_page

    def get_all_conferences(self) -> list[Conference]:
        return [Conference(**c) for c in self._conferences()]

    def get_conferences_from_timeframe(self, start_time: datetime):
        return [Conference(**c) for c in self._conferences(start_time.timestamp())]

    def get_conference(self, conference_id: str) -> Optional[Conference]:
        res = requests.get(f"https://www.bigmarker.com/api/v1/conferences/{conference_id}",
                           headers=self._headers)
        if res.status_code != 200:
            return None
        return Conference(**res.json())

    def search_conference(self,
                          title: Optional[str] = None,
                          start_time: Optional[str] = None,
                          end_time: Optional[str] = None,
                          conference_ids: Optional[list[str]] = None,
                          presenter_member_ids: Optional[str] = None,
                          role: Optional[Literal['hosting', 'attending', 'all']] = None) -> Optional[list[Conference]]:
        all_search_params: dict = {
            'title': title,
            'start_time': start_time,
            'end_time': end_time,
            'conference_ids': ",".join(conference_ids) if conference_ids else None,
            'presenter_ids': ",".join(presenter_member_ids) if presenter_member_ids else None,
            'role': role
        }
        search_parameters: dict = {k: v for k, v in all_search_params.items() if v is not None}
        return [Conference(**c) for c in self._conferences_search(search_parameters)]

    def get_associated_conferences(self, conference_id: str) -> list[Conference]:
        return [Conference(**c) for c in self._conferences(
            url=f"https://www.bigmarker.com/api/v1/conferences/get_associated_sessions/{conference_id}")]

    def get_recurring_conferences(self, conference_id: str) -> list[Conference]:
        return [Conference(**c) for c in self._conferences(
            url=f"https://www.bigmarker.com/api/v1/conferences/recurring/{conference_id}")]

    def create_conference(self,
                          channel_id: str,
                          title: str,
                          conference_copy_id: Optional[str] = None,
                          presenter_exit_url: Optional[HttpUrl] = None,
                          sub_url: Optional[HttpUrl] = None,
                          enable_dial_in: Optional[bool] = None,
                          purpose: Optional[str] = None,
                          time_zone: Optional[Timezone] = None,
                          room_logo: Optional[HttpUrl] = None,
                          conference_logo: Optional[HttpUrl] = None,
                          apply_conference_logo_to_channel: Optional[bool] = None,
                          room_sub_title: Optional[str] = None,
                          schedule_type: Optional[Literal["24_hour_room", "one_time"]] = None,
                          start_time: datetime = None,
                          recurring_start_times: list[datetime] = None,
                          webcast_mode: Optional[Literal["automatic", "required", "optional"]] = None,
                          duration_minutes: Optional[int] = None,
                          who_can_watch_recording: Optional[
                              Literal[
                                  "everyone", "channel_admin_only", "channel_subscribers", "attendees", "attendees_registrants"]] = None,
                          presenter_advanced_enter_time: Optional[Literal["60", "120", "180"]] = None,
                          attendee_advanced_enter_time: Optional[Literal["15", "30"]] = None,
                          privacy: Optional[Literal["private", "public"]] = None,
                          webinar_format: Optional[Literal["webinar", "livestream", "on_demand"]] = None,
                          ondemand_video_url: Optional[HttpUrl] = None,
                          enable_knock_to_enter: Optional[bool] = None,
                          registration_conf_emails: Optional[bool] = None,
                          send_notification_emails_to_presenters: Optional[bool] = None,
                          send_reminder_emails_to_presenters: Optional[bool] = None,
                          show_reviews: Optional[bool] = None,
                          review_emails: Optional[bool] = None,
                          poll_results: Optional[bool] = None,
                          enable_ie_safari: Optional[bool] = None,
                          enable_twitter: Optional[bool] = None,
                          send_cancellation_email: Optional[bool] = None,
                          webhook_url: Optional[HttpUrl] = None,
                          exit_url: Optional[HttpUrl] = None,
                          enable_create_webinar_reg_webhook: Optional[bool] = None,
                          enable_new_reg_webhook: Optional[bool] = None,
                          new_reg_webhook_url: Optional[HttpUrl] = None,
                          enable_webinar_start_webhook: Optional[bool] = None,
                          webinar_start_webhook_url: Optional[HttpUrl] = None,
                          enable_waiting_room_open_webhook: Optional[bool] = None,
                          waiting_room_open_webhook_url: Optional[HttpUrl] = None,
                          enable_webinar_end_webhook: Optional[bool] = None,
                          webinar_end_webhook_url: Optional[HttpUrl] = None,
                          enable_live_attendee_data_webhook: Optional[bool] = None,
                          live_attendee_data_webhook_url: Optional[HttpUrl] = None,
                          enable_on_demand_viewer_webhook: Optional[bool] = None,
                          on_demand_viewer_webhook_url: Optional[HttpUrl] = None,
                          registration_required_to_view_recording: Optional[bool] = None,
                          channel_admin_id: Optional[str] = None,
                          background_image_url: Optional[HttpUrl] = None,
                          room_type: Optional[Literal["1", "attendee_as_presenter", "attendee_mic_and_cam"]] = None,
                          display_language: Optional[str] = None,
                          show_handout_on_page: Optional[bool] = None,
                          banner_filter_percentage: Optional[int] = None,
                          icon: Optional[HttpUrl] = None,
                          webinar_tags: Optional[dict[str, str]] = None) -> Conference:

        conference = ConferenceCreate(
            channel_id=channel_id,
            title=title,
            conference_copy_id=conference_copy_id,
            presenter_exit_url=presenter_exit_url,
            sub_url=sub_url,
            enable_dial_in=enable_dial_in,
            purpose=purpose,
            time_zone=time_zone,
            room_logo=room_logo,
            conference_logo=conference_logo,
            apply_conference_logo_to_channel=apply_conference_logo_to_channel,
            room_sub_title=room_sub_title,
            schedule_type=schedule_type,
            start_time=start_time,
            recurring_start_times=recurring_start_times,
            webcast_mode=webcast_mode,
            duration_minutes=duration_minutes,
            who_can_watch_recording=who_can_watch_recording,
            presenter_advanced_enter_time=presenter_advanced_enter_time,
            attendee_advanced_enter_time=attendee_advanced_enter_time,
            privacy=privacy,
            webinar_format=webinar_format,
            ondemand_video_url=ondemand_video_url,
            enable_knock_to_enter=enable_knock_to_enter,
            registration_conf_emails=registration_conf_emails,
            send_notification_emails_to_presenters=send_notification_emails_to_presenters,
            send_reminder_emails_to_presenters=send_reminder_emails_to_presenters,
            show_reviews=show_reviews,
            review_emails=review_emails,
            poll_results=poll_results,
            enable_ie_safari=enable_ie_safari,
            enable_twitter=enable_twitter,
            send_cancellation_email=send_cancellation_email,
            webhook_url=webhook_url,
            exit_url=exit_url,
            enable_create_webinar_reg_webhook=enable_create_webinar_reg_webhook,
            enable_new_reg_webhook=enable_new_reg_webhook,
            new_reg_webhook_url=new_reg_webhook_url,
            enable_webinar_start_webhook=enable_webinar_start_webhook,
            webinar_start_webhook_url=webinar_start_webhook_url,
            enable_waiting_room_open_webhook=enable_waiting_room_open_webhook,
            waiting_room_open_webhook_url=waiting_room_open_webhook_url,
            enable_webinar_end_webhook=enable_webinar_end_webhook,
            webinar_end_webhook_url=webinar_end_webhook_url,
            enable_live_attendee_data_webhook=enable_live_attendee_data_webhook,
            live_attendee_data_webhook_url=live_attendee_data_webhook_url,
            enable_on_demand_viewer_webhook=enable_on_demand_viewer_webhook,
            on_demand_viewer_webhook_url=on_demand_viewer_webhook_url,
            registration_required_to_view_recording=registration_required_to_view_recording,
            channel_admin_id=channel_admin_id,
            background_image_url=background_image_url,
            room_type=room_type,
            display_language=display_language,
            show_handout_on_page=show_handout_on_page,
            banner_filter_percentage=banner_filter_percentage,
            icon=icon,
            webinar_tags=webinar_tags
        )
        res = self._session.post(f"https://www.bigmarker.com/api/v1/conferences",
                                 headers=self._headers,
                                 json=conference.model_dump_json(exclude_none=True)).json()
        if res.status_code != 201:
            raise Exception(res.text)
        return Conference(**res)

    def update_conference(self,
                          conference_id: str,
                          title: str,
                          presenter_exit_url: Optional[HttpUrl] = None,
                          sub_url: Optional[HttpUrl] = None,
                          enable_dial_in: Optional[bool] = None,
                          purpose: Optional[str] = None,
                          time_zone: Optional[Timezone] = None,
                          room_logo: Optional[HttpUrl] = None,
                          conference_logo: Optional[HttpUrl] = None,
                          apply_conference_logo_to_channel: Optional[bool] = None,
                          room_sub_title: Optional[str] = None,
                          schedule_type: Optional[Literal["24_hour_room", "one_time"]] = None,
                          start_time: datetime = None,
                          recurring_start_times: list[datetime] = None,
                          webcast_mode: Optional[Literal["automatic", "required", "optional"]] = None,
                          duration_minutes: Optional[int] = None,
                          who_can_watch_recording: Optional[
                              Literal[
                                  "everyone", "channel_admin_only", "channel_subscribers", "attendees", "attendees_registrants"]] = None,
                          presenter_advanced_enter_time: Optional[Literal["60", "120", "180"]] = None,
                          attendee_advanced_enter_time: Optional[Literal["15", "30"]] = None,
                          privacy: Optional[Literal["private", "public"]] = None,
                          webinar_format: Optional[Literal["webinar", "livestream", "on_demand"]] = None,
                          ondemand_video_url: Optional[HttpUrl] = None,
                          enable_knock_to_enter: Optional[bool] = None,
                          registration_conf_emails: Optional[bool] = None,
                          send_notification_emails_to_presenters: Optional[bool] = None,
                          send_reminder_emails_to_presenters: Optional[bool] = None,
                          show_reviews: Optional[bool] = None,
                          review_emails: Optional[bool] = None,
                          poll_results: Optional[bool] = None,
                          enable_ie_safari: Optional[bool] = None,
                          enable_twitter: Optional[bool] = None,
                          send_cancellation_email: Optional[bool] = None,
                          webhook_url: Optional[HttpUrl] = None,
                          exit_url: Optional[HttpUrl] = None,
                          enable_create_webinar_reg_webhook: Optional[bool] = None,
                          enable_new_reg_webhook: Optional[bool] = None,
                          new_reg_webhook_url: Optional[HttpUrl] = None,
                          enable_webinar_start_webhook: Optional[bool] = None,
                          webinar_start_webhook_url: Optional[HttpUrl] = None,
                          enable_waiting_room_open_webhook: Optional[bool] = None,
                          waiting_room_open_webhook_url: Optional[HttpUrl] = None,
                          enable_webinar_end_webhook: Optional[bool] = None,
                          webinar_end_webhook_url: Optional[HttpUrl] = None,
                          enable_live_attendee_data_webhook: Optional[bool] = None,
                          live_attendee_data_webhook_url: Optional[HttpUrl] = None,
                          enable_on_demand_viewer_webhook: Optional[bool] = None,
                          on_demand_viewer_webhook_url: Optional[HttpUrl] = None,
                          registration_required_to_view_recording: Optional[bool] = None,
                          channel_admin_id: Optional[str] = None,
                          background_image_url: Optional[HttpUrl] = None,
                          room_type: Optional[Literal["1", "attendee_as_presenter", "attendee_mic_and_cam"]] = None,
                          display_language: Optional[str] = None,
                          show_handout_on_page: Optional[bool] = None,
                          banner_filter_percentage: Optional[int] = None,
                          icon: Optional[HttpUrl] = None,
                          webinar_tags: Optional[dict[str, str]] = None) -> Conference:

        conference = ConferenceCreate(
            title=title,
            presenter_exit_url=presenter_exit_url,
            sub_url=sub_url,
            enable_dial_in=enable_dial_in,
            purpose=purpose,
            time_zone=time_zone,
            room_logo=room_logo,
            conference_logo=conference_logo,
            apply_conference_logo_to_channel=apply_conference_logo_to_channel,
            room_sub_title=room_sub_title,
            schedule_type=schedule_type,
            start_time=start_time,
            recurring_start_times=recurring_start_times,
            webcast_mode=webcast_mode,
            duration_minutes=duration_minutes,
            who_can_watch_recording=who_can_watch_recording,
            presenter_advanced_enter_time=presenter_advanced_enter_time,
            attendee_advanced_enter_time=attendee_advanced_enter_time,
            privacy=privacy,
            webinar_format=webinar_format,
            ondemand_video_url=ondemand_video_url,
            enable_knock_to_enter=enable_knock_to_enter,
            registration_conf_emails=registration_conf_emails,
            send_notification_emails_to_presenters=send_notification_emails_to_presenters,
            send_reminder_emails_to_presenters=send_reminder_emails_to_presenters,
            show_reviews=show_reviews,
            review_emails=review_emails,
            poll_results=poll_results,
            enable_ie_safari=enable_ie_safari,
            enable_twitter=enable_twitter,
            send_cancellation_email=send_cancellation_email,
            webhook_url=webhook_url,
            exit_url=exit_url,
            enable_create_webinar_reg_webhook=enable_create_webinar_reg_webhook,
            enable_new_reg_webhook=enable_new_reg_webhook,
            new_reg_webhook_url=new_reg_webhook_url,
            enable_webinar_start_webhook=enable_webinar_start_webhook,
            webinar_start_webhook_url=webinar_start_webhook_url,
            enable_waiting_room_open_webhook=enable_waiting_room_open_webhook,
            waiting_room_open_webhook_url=waiting_room_open_webhook_url,
            enable_webinar_end_webhook=enable_webinar_end_webhook,
            webinar_end_webhook_url=webinar_end_webhook_url,
            enable_live_attendee_data_webhook=enable_live_attendee_data_webhook,
            live_attendee_data_webhook_url=live_attendee_data_webhook_url,
            enable_on_demand_viewer_webhook=enable_on_demand_viewer_webhook,
            on_demand_viewer_webhook_url=on_demand_viewer_webhook_url,
            registration_required_to_view_recording=registration_required_to_view_recording,
            channel_admin_id=channel_admin_id,
            background_image_url=background_image_url,
            room_type=room_type,
            display_language=display_language,
            show_handout_on_page=show_handout_on_page,
            banner_filter_percentage=banner_filter_percentage,
            icon=icon,
            webinar_tags=webinar_tags
        )
        res = self._session.put(f"https://www.bigmarker.com/api/v1/conferences/{conference_id}",
                                headers=self._headers,
                                json=conference.model_dump_json(exclude_none=True)).json()
        if res.status_code != 201:
            raise Exception(res.text)
        return Conference(**res)

    def upload_preloaded_file(self,
                              conference_id: str,
                              file_url: HttpUrl,
                              autoplay: Optional[bool] = None) -> UploadFileStatus:
        res = self._session.put(url=f"https://www.bigmarker.com/api/v1/conferences/{conference_id}/upload_file",
                                headers=self._headers,
                                date={
                                    "file_url": file_url,
                                    "autoplay": autoplay
                                })

        if res.status_code != 201:
            return UploadFileStatus(
                success=False,
                message=res.json()["error"]
            )

        return UploadFileStatus(
            success=True,
            message=res.json()['success'],
            id=res.json()['id'],
            type=res.json()['file_type']
        )

    def delete_preloaded_file(self,
                              conference_id: str,
                              file_id: str) -> FileStatus:
        res = self._session.put(
            url=f"https://www.bigmarker.com/api/v1/conferences/{conference_id}/upload_file/delete_file/{file_id}",
            headers=self._headers)

        if res.status_code != 201:
            return FileStatus(
                success=False,
                message=res.json()["error"]
            )

        return FileStatus(
            success=True,
            message=res.json()['success']
        )
