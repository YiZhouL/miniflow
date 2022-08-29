import typing as T
import asyncio
import datetime

E8 = datetime.timezone(datetime.timedelta(hours=8))
_timer = T.TypeVar("_timer", "Timer", None, int)


class Timer:
    def __init__(self, end_time: datetime.datetime = None, tz=None):
        self._tz = tz or E8
        if end_time and self._end_time.tzinfo is None:
            self._end_time = end_time.replace(tzinfo=self._tz)
        else:
            self._end_time = datetime.datetime.max.replace(tzinfo=self._tz)

    async def sleep(self):
        await asyncio.sleep(self._get_sleep_second())

    @property
    def is_end(self):
        return datetime.datetime.now(tz=self._tz) + datetime.timedelta(seconds=self._get_sleep_second(is_next=False)) \
               > self._end_time

    def _get_sleep_second(self, is_next=True) -> int:
        raise NotImplemented


class EqualTimer(Timer):
    def __init__(self, second, end_time=None, tz=None):
        super().__init__(end_time, tz)
        if second < 0:
            raise ValueError("second need equal or more than 0.")
        else:
            self._second = second

    def _get_sleep_second(self, is_next=True) -> int:
        return self._second


class OnceTimer(EqualTimer):
    def _get_sleep_second(self, is_next=True) -> int:
        if is_next:
            self._end_time = datetime.datetime.min.replace(tzinfo=self._tz)
        return self._second
