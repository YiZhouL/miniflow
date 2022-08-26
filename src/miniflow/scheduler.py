import asyncio
import typing as T

from .simpleprocess import SimpleProcess
from .timer import Timer, OnceTimer, EqualTimer


def _remove_job_scheduler(job, scheduler):
    job._owners.remove(scheduler)


class Scheduler(SimpleProcess):
    def __init__(self, startup=False):
        super().__init__(startup)

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
                    asyncio.get_event_loop().create_task(job.run())
                    await timer.sleep()
                else:
                    await asyncio.sleep(1)

        if not self.stopped and not job.stopped:
            asyncio.get_event_loop().create_task(_register_job())

    def start(self):
        super().start()

        async def run_forever():
            while True:
                if self.stopped:
                    break
                await asyncio.sleep(2)
        asyncio.get_event_loop().run_until_complete(run_forever())
