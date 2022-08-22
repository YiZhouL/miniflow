import asyncio
import typing as T

from .simpleprocess import SimpleProcess
from .timer import Timer, OnceTimer, EqualTimer


def _remove_job_scheduler(job, scheduler):
    job._owners.remove(scheduler)


class Scheduler(SimpleProcess):
    def __init__(self):
        super().__init__()

    def add_job(self, job, timer: T.Union[Timer, int, None] = None):
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
                    asyncio.create_task(job.run())
                    await timer.sleep()
                else:
                    await asyncio.sleep(1)

        if not self.stopped and not job.stopped:
            asyncio.create_task(_register_job())
