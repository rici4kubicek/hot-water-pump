"""
Interval/periodic measurements
"""

from .monotonic import monotonic

__all__ = ["Interval"]


class Interval(object):
    __slots__ = ('_start_time', '_reload')

    def __init__(self, value=0, expired=False):
        self._start_time = int(monotonic())
        self._reload = value
        if expired:
            self._start_time -= self._reload

    def __str__(self):
        return 'Interval(period={},remain={},expired={})'.format(self._reload, self.reminding, self.is_expired)

    @property
    def reminding(self):
        """
        Reminding time to expiration in seconds
        :return:
        """
        if self._reload is None:
            return 0
        return self._reload - (int(monotonic() - self._start_time))

    @property
    def is_expired(self):
        """
        Check if interval is expired
        :return:
        """
        if self._reload is None:
            return None
        return int(monotonic()) >= self._start_time + self._reload

    def restart(self):
        """
        Restart timer from now
        """
        self._start_time = int(monotonic())

    def set(self, value):
        """
        Set reload value and start interval
        :param value:
        :return:
        """
        self._reload = value
        self.restart()

    def restarted(self):
        """
        Check if interval is expired and if so, auto reload
        :return:
        """
        if self.is_expired:
            self.restart()
            return True
        return False