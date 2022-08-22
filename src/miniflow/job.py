import typing as T
import asyncio

from .simpleprocess import SimpleProcess


class Job(SimpleProcess):
    def __init__(self,
                 pipelines: T.Iterable[T.Any] = None,
                 owners: T.Iterable[T.Any] = None
                 ):
        self._owners = set([owner for owner in owners if not owner.stopped]) if owners else set()
        self._pipelines = set([pipe for pipe in pipelines if not pipe.stopped]) if pipelines else set()
        super().__init__()

    def start(self):
        super().start()
        [owner.add_job(self) for owner in self._owners]
        [pipe.add_job(self) for pipe in self._pipelines]

    async def run(self):
        data: T.List[T.Any] = await self._run()
        [asyncio.create_task(pipeline.execute(data)) for pipeline in self._pipelines if pipeline.started]

    async def _run(self) -> []:
        raise NotImplemented

    def add_pipeline(self, pipe):
        if not pipe.stopped:
            self._pipelines.add(pipe)

    def add_scheduler(self, scheduler, timer=None):
        if not scheduler.stopped and scheduler not in self._owners:
            self._owners.add(scheduler)
            scheduler.add_job(self, timer)

    def stop(self):
        super().stop()
        self._pipelines.clear()
        self._owners.clear()
