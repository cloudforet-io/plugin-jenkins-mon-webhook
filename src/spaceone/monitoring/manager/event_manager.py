import logging
import datetime
from spaceone.core.manager import BaseManager
from spaceone.core.utils import random_string
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *

_LOGGER = logging.getLogger(__name__)
DEFAULT_TITLE = 'Generate Notification'


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, data):
        """ data sample
            "event": {}
        """
        try:
            _LOGGER.debug("-----")
            _LOGGER.debug(data)
            _LOGGER.debug("-----")

            event_dict = {
                'event_key': self._generate_event_key(data.get('url')),
                'event_type': self._set_event_type(data),
                'severity': self._set_severity(data),
                'resource': {},
                'title': self._set_title(data),
                'description': self._set_description(data),
                'rule': '',
                'occurred_at': self._set_occurred_at(data),
                'additional_info': self._set_additional_info(data)
            }

            event_model = EventModel(event_dict, strict=False)
            event_model.validate()
            return [event_model.to_native()]

        except Exception as e:
            raise ERROR_EVENT_PARSE()

    @staticmethod
    def _generate_event_key(url):
        if url:
            return url
        else:
            return random_string()

    @staticmethod
    def _set_severity(data):
        severity = 'INFO'

        if data.get('build', {}).get('status') == 'FAILURE':
            severity = 'ERROR'

        return severity

    @staticmethod
    def _set_event_type(data):
        event_type = 'ALERT'

        if data.get('build', {}).get('status') == 'FAILURE':
            event_type = 'ERROR'

        return event_type

    @staticmethod
    def _set_title(data):
        return f'[Jenkins] Build - {data.get("display_name")}'

    @staticmethod
    def _set_description(data):
        description = "Build Notifications\n\n"
        build = data.get('build', {})

        if data.get('name'):
            description = f'{description} - Name: {data["name"]}\n'

        if build.get('number'):
            description = f'{description} - Build Number: {build["number"]}\n'

        if data.get('url'):
            description = f'{description} - URL: {data["url"]}\n'

        if build.get('phase'):
            description = f'{description} - Build Phase: {build["phase"]}\n'

        if build.get('status'):
            description = f'{description} - Build Status: {build["status"]}\n'

        if build.get('duration'):
            description = f'{description} - Build Duration: {build["duration"]} Sec.\n'

        return description

    @staticmethod
    def _set_occurred_at(data):
        occurred_at = None

        if timestamp := data.get('build', {}).get('timestamp'):
            occurred_at = datetime.datetime.fromtimestamp(timestamp/1000)

        return occurred_at

    @staticmethod
    def _set_additional_info(data):
        info = {}
        build = data.get('build', {})

        info.update({'build_no': build.get('number')})
        info.update({'url': data.get('url')})
        info.update({'full_url': build.get('full_url')})
        info.update({'build_phase': build.get('phase')})
        info.update({'build_status': build.get('status')})
        info.update({'build_duration': build.get('duration')})

        if log := build.get('log'):
            info.update({'log': log})

        if notes := build.get('notes'):
            info.update({'notes': notes})

        if 'scm' in build:
            info.update({'scm': build['scm']})

        if 'artifacts' in build:
            info.update({'artifacts': build['artifacts']})

        info.update({'timestamp': build.get('timestamp')})

        return info
