import asyncio
import typing as T
from threading import local

from .simpleprocess import SimpleProcess
from .job import Job
from .timer import OnceTimer, EqualTimer, _timer

_all_schedulers = local()


def get_current_schedulers() -> T.Set["Scheduler"]:
    if not hasattr(_all_schedulers, "obj"):
        _all_schedulers.obj = {Scheduler()}
    return _all_schedulers.obj


def create_new_scheduler() -> "Scheduler":
    new = Scheduler()
    if not hasattr(_all_schedulers, "obj"):
        _all_schedulers.obj = {new}
    else:
        _all_schedulers.obj.add(new)
    return new


def _remove_job_scheduler(job, scheduler):
    job._owners.remove(scheduler)


def _add_job_scheduler(job, scheduler):
    job._owners.add(scheduler)


class Scheduler(SimpleProcess):
    def __init__(self, startup=False):
        super().__init__(startup)

    def add_job(self, job, timer: _timer = None):
        if timer is None:
            timer = OnceTimer(0)
        elif isinstance(timer, int):
            timer = EqualTimer(timer)

        async def _register_job():
            while True:
                if self.stopped:
                    _remove_job_scheduler(job, self)
                    break
                elif job.stopped:
                    break
                elif timer.is_end:
                    job.stop()
                    break
                elif self.started and job.started:
                    asyncio.get_event_loop().create_task(job.run())
                    await timer.sleep()
                else:
                    await asyncio.sleep(1)

        if not self.stopped and not job.stopped:
            _add_job_scheduler(job, self)
            asyncio.get_event_loop().create_task(_register_job())

    def stop(self):
        super().stop()
        get_current_schedulers().remove(self)   # if exists

    def __call__(self, timer: _timer) -> T.Callable[[Job], Job]:
        from .register import register_job

        return register_job(timer, self)


def start():
    [sch.start() for sch in get_current_schedulers()]

    async def run_forever():
        while True:
            if all([sch.stopped for sch in get_current_schedulers()]):
                break
            await asyncio.sleep(2)

    asyncio.get_event_loop().run_until_complete(run_forever())


def stop():
    [super(Scheduler, sch).stop() for sch in get_current_schedulers()]
    get_current_schedulers().clear()


def pause():
    [sch.pause() for sch in get_current_schedulers()]
