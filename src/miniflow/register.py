import typing as T

from .scheduler import Scheduler, get_current_schedulers
from .job import Job
from .timer import _timer

_Job = T.TypeVar("_Job")


def register_func(timer_: _timer = None, scheduler: Scheduler = None):
    def wrapper_job(do_something: T.Callable[[_Job], T.Coroutine]) -> _Job:
        async def _run(self: Job) -> T.Union[T.List[T.Any], None]:
            return await do_something(self)

        j = type("WrapperJob({})".format(do_something.__name__), (Job, ), {"_run": _run})

        if scheduler is None:
            [sch.add_job(j(), timer_) for sch in get_current_schedulers()]
        else:
            scheduler.add_job(j(), timer_)
        return j
    return wrapper_job


def register_job(timer: _timer = None, scheduler: Scheduler = None):
    def wrapper_job(j: _Job) -> Job:
        if scheduler is None:
            [sch.add_job(j(), timer) for sch in get_current_schedulers()]
        else:
            scheduler.add_job(j(), timer)
        return j
    return wrapper_job
