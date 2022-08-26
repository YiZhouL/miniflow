import typing as T
from threading import local

from .scheduler import Scheduler
from .job import Job
from .pipeline import PipeLine
from .timer import Timer

_scheduler = local()


def get_current_scheduler() -> Scheduler:
    if not hasattr(_scheduler, "obj"):
        _scheduler.obj = Scheduler()
    return _scheduler.obj


def register_func(timer_: T.Union[Timer, int, None]):
    def wrapper_job(do_something: T.Callable[[Job], T.Union[T.List[T.Any], None]]):
        async def _run(self) -> T.Union[T.List[T.Any], None]:
            return await do_something(self)

        j = type("WrapperJob({})".format(do_something.__name__), (Job, ), {"_run": _run})

        get_current_scheduler().add_job(j(), timer_)
    return wrapper_job


def register_job(timer_: T.Union[Timer, int, None]):
    def wrapper_job(j: T.Callable[[], Job]):
        get_current_scheduler().add_job(j(), timer_)
    return wrapper_job


def start():
    get_current_scheduler().start()


def stop():
    get_current_scheduler().stop()
