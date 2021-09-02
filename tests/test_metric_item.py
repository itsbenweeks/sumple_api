from datetime import datetime, timedelta
import unittest

from dateutil.parser import parse
from freezegun import freeze_time

from sumple_api.metric_item import MetricItem, MetricItems


class HappyMetricItemTest(unittest.TestCase):
    def test_date_field(self):
        with freeze_time("August 8th, 2021, 6:00pm"):
            test_datetime = datetime.now()
            item = MetricItem(value=1, date=datetime.now())
        self.assertEqual(
            str(item.date), str(test_datetime), f"`item.date` should be {test_datetime}"
        )

    def test_value_field(self):
        item = MetricItem(value=1)
        self.assertEqual(item.value, 1, "`item.value` should be 1")


class UnhappyMetricItemTest(unittest.TestCase):
    def test_value_exception(self):
        self.assertRaises(ValueError, MetricItem, **{"value": "Not an integer"})

    def test_date_exception(self):
        self.assertRaises(
            ValueError, MetricItem, **{"value": 1, "date": "Not a datetime"}
        )


class HappyMetricItemsTest(unittest.TestCase):
    def setUp(self):
        test_date = parse("August 8th, 2021, 6:00pm")
        self.item1 = MetricItem(value=1, date=test_date)
        self.item2 = MetricItem(value=2, date=test_date + timedelta(minutes=20))
        self.item3 = MetricItem(value=3, date=test_date + timedelta(minutes=40))

    def test_metric_items(self):
        items = MetricItems(data=[self.item1, self.item2, self.item3])
        self.assertEqual(items.data, [self.item1, self.item2, self.item3])

    def test_metric_items_sort(self):
        items = MetricItems(data=[self.item2, self.item1, self.item3])
        self.assertEqual(items.data, [self.item2, self.item1, self.item3])
        items.sort()
        print(f"{items}")
        self.assertEqual(items.data, [self.item1, self.item2, self.item3])

    def test_metric_items_purge(self):
        items = MetricItems(data=[self.item1, self.item2, self.item3])
        self.assertEqual(items.data, [self.item1, self.item2, self.item3])
        with freeze_time("August 8th, 2021, 7:10pm"):
            items.purge(filter_date=datetime.now() - timedelta(hours=1))
            self.assertEqual(items.data, [self.item2, self.item3])
        with freeze_time("August 8th, 2021, 7:30pm"):
            items.purge(filter_date=datetime.now() - timedelta(hours=1))
            self.assertEqual(items.data, [self.item3])

    def test_metric_items_append(self):
        items = MetricItems(data=[self.item1, self.item2, self.item3])
        self.assertEqual(items.data, [self.item1, self.item2, self.item3])
        with freeze_time("August 8th, 2021, 6:45pm") as ft:
            item4 = MetricItem(value=4)
        items.append(item4)
        self.assertEqual(items.data, [self.item1, self.item2, self.item3, item4])


class UnhappyMetricItemsTest(unittest.TestCase):
    def setUp(self):
        with freeze_time("August 8th, 2021, 6:00pm") as ft:
            self.item1 = MetricItem(value=1)
            ft.tick(delta=timedelta(minutes=20))
            self.item2 = MetricItem(value=2)
            ft.tick(delta=timedelta(minutes=20))
            self.item3 = MetricItem(value=3)

    def test_metric_items_value_errors(self):
        self.assertRaises(
            ValueError, MetricItems, **{"data": (self.item1, self.item2, self.item3)}
        )
        self.assertRaises(ValueError, MetricItems, **{"data": [1, 2, 3]})
