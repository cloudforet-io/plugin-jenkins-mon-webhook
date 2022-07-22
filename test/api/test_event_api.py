import logging
import unittest
import os
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.tester import TestCase, print_json

_LOGGER = logging.getLogger(__name__)
TEST_JSON = os.environ.get('test_json', None)


class TestEvent(TestCase):

    def test_parse(self):
        params = {
            'options': {},
            'data': {"build": {"status": "SUCCESS", "log": "", "queue_id": 24.0, "url": "job/Freestyle%20Job%201/12/", "notes": "", "scm": {"culprits": [], "changes": []}, "phase": "FINALIZED", "artifacts": {}, "full_url": "http://13.124.148.140:8080/job/Freestyle%20Job%201/12/", "timestamp": 1658465683072.0, "duration": 182.0, "number": 12.0}, "name": "Freestyle Job 1", "display_name": "Freestyle Job 1", "url": "job/Freestyle%20Job%201/"}
        }

        test_cases = [params]

        for idx, test_case in enumerate(test_cases):
            print(f'###### {idx} ########')
            parsed_data = self.monitoring.Event.parse({'options': {}, 'data': test_case.get('data')})
            print_json(parsed_data)
            print()


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
