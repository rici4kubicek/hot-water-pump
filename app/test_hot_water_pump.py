from app.hot_water_pump import HotWaterPumpLib
import json
import pytest


class MyDateTime:
    _hour = 0
    _minute = 0
    _weekday = 0

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, hour):
        self._hour = hour

    @property
    def minute(self):
        return self._minute

    @minute.setter
    def minute(self, minute):
        self._minute = minute

    def weekday(self):
        return self._weekday

    def set_weekday(self, wd):
        self._weekday = wd


@pytest.mark.parametrize("hour, minute, weekday, state", [
    (4, 1, 0, True),
    (3, 59, 0, False),
    (6, 0, 0, True),
    (6, 1, 0, False),
    (21, 30, 0, True),
    (21, 31, 0, False),
    (9, 0, 5, True),
    (9, 1, 5, False),
    (10, 59, 5, False),
    (11, 0, 5, True),
])
def test_check_time_mask(hour, minute, weekday, state):
    config = {}
    with open('../data/config.json') as f:
        config = json.load(f)
    pump = HotWaterPumpLib(config)

    dt = MyDateTime()
    dt.hour = hour
    dt.minute = minute
    dt.set_weekday(weekday)

    assert pump.check_time_mask(dt) == state

