import unittest

from freezegun import freeze_time

from sumple_api.app import app as flask_app
import sumple_api.app as app
from sumple_api.metric_item import MetricItem, MetricItems


class HappyAPITest(unittest.TestCase):
    def setUp(self):
        flask_app.config["TESTING"] = True

    def test_post(self):
        with flask_app.test_client() as client:
            with freeze_time("August 7th, 2021, 5:00pm"):
                post_response = client.post("metric/foo", json={"value": 2})
                self.assertIn("foo", app.DATA.keys(), "'foo' entry not added to DATA!")
                self.assertEqual(
                    1, len(app.DATA["foo"].data), "1 entry not in DATA['foo']!"
                )
                self.assertEqual(
                    type(MetricItems()),
                    type(app.DATA["foo"]),
                    "app.DATA['foo'] entry isn't of type MetricItems!",
                )
                self.assertEqual(
                    type(MetricItem(0)),
                    type(app.DATA["foo"].data[0]),
                    "app.DATA['foo'].data entry isn't of type MetricItem!",
                )
            self.assertEqual(post_response.status_code, 200)

    def test_sum(self):
        with flask_app.test_client() as client:
            with freeze_time("August 8th, 2021, 5:00pm"):
                client.post("metric/foo", json={"value": 2})
            with freeze_time("August 8th, 2021, 6:00pm"):
                client.post("metric/bar", json={"value": 1})
            with freeze_time("August 8th, 2021, 6:10pm"):
                client.post("metric/baz", json={"value": 2})
            with freeze_time("August 8th, 2021, 6:15pm"):
                client.post("metric/bar", json={"value": 3})
            with freeze_time("August 8th, 2021, 6:30pm"):
                client.post("metric/baz", json={"value": 4})
            with freeze_time("August 8th, 2021, 6:35pm"):
                foo_response = client.get("metric/foo/sum")
                bar_response = client.get("metric/bar/sum")
                baz_response = client.get("metric/baz/sum")
                self.assertEqual(foo_response.json, {"value": 0})
                self.assertEqual(bar_response.json, {"value": 4})
                self.assertEqual(baz_response.json, {"value": 6})


class UnhappyAPITest(unittest.TestCase):
    def setUp(self):
        flask_app.config["TESTING"] = True

    def test_post(self):
        with flask_app.test_client() as client:
            post_response = client.post("metric/foo", json={"value": "not_a_value"})
            self.assertEqual(post_response.status_code, 400)
            post_response = client.post("metric/foo", json={"bad": "json"})
            self.assertEqual(post_response.status_code, 400)

    def test_get(self):
        with flask_app.test_client() as client:
            get_response = client.get("metric/bad/sum")
            self.assertEqual(get_response.status_code, 400)
