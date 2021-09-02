from dataclasses import dataclass, field
from datetime import datetime, timedelta
from importlib import util
import operator


@dataclass
class MetricItem(object):
    """Class to store metric keys to easily gather sum. Sortable by time,
    can perform arthmetic with value."""

    value: int
    date: datetime = datetime.now()

    def __lt__(self, other):
        return self.date < other.date

    def __post_init__(self):
        # work around freezegun's FakeDateTime class
        # condition only passes if test_requirement.txt are installed
        if util.find_spec("freezegun"):
            from dateutil.parser import parse

            self.date = parse(str(self.date))
        if type(self.value) != type(int(0)):
            raise ValueError("value is not an int")
        if type(self.date) != type(datetime.now()):
            print(f"{type(self.date)=}")
            print(f"{type(datetime.now())}")
            raise ValueError("date is not a datetime")


@dataclass
class MetricItems(object):
    """Class to contain each of the metric items with a little helper method to
    trim items more than an hour old."""

    data: list[MetricItem] = field(default_factory=list)

    def __post_init__(self):
        if type(self.data) != type(list()):
            print(f"{type(self.data)=}")
            print(f"{type(list())=}")
            raise ValueError("data is not a list")
        for value in self.data:
            if type(value) != type(MetricItem(value=0)):
                raise ValueError("data is not a list of MetricItem objects")

    def append(self, *args, **kwargs):
        """Passthrough function to self.data.append"""
        self.data.append(*args, **kwargs)

    def purge(self, filter_date=(datetime.now() - timedelta(hours=1))):
        """
        Purge any MetricItem older than one hour.
        """
        self.data.sort(key=operator.attrgetter("date"))
        for i, metric_item in enumerate(self.data):
            if metric_item.date >= filter_date:
                self.data = self.data[i:]
                return
        self.data = []
        return

    def sort(self, *args, **kwargs):
        """Passthrough function to self.data.sort"""
        if "key" not in kwargs.keys():
            self.data = sorted(self.data, key=operator.attrgetter("date"))
        else:
            self.data.sort(*args, **kwargs)
