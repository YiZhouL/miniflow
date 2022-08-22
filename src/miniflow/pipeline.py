import typing as T
import asyncio

from .simpleprocess import SimpleProcess


class AsyncConsumer(SimpleProcess):
    def __init__(self, num=1, only_execute=False):
        self._only_execute = only_execute
        self._consumer_num = num
        self._consumer_queue = asyncio.queues.Queue()
        super().__init__()

    async def push(self, data: T.List[T.Any]):
        await self._consumer_queue.put(data)

    async def execute(self, data: T.List[T.Any]):
        try:
            await self._execute(data)
        except (Exception, BaseException):
            if not self._only_execute:
                await self.push(data)
        else:
            pass

    async def _execute(self, data: T.List[T.Any]):
        raise NotImplemented

    async def execute_forever(self):
        while True:
            if self.stopped:
                break
            elif self.started and not self._consumer_queue.empty():
                data = await self._consumer_queue.get()
                self._consumer_queue.task_done()
                await self.execute(data)
            else:
                await asyncio.sleep(1)

    def start(self):
        if not self._only_execute:
            [asyncio.create_task(self.execute_forever()) for i in range(self._consumer_num)]
        super().start()


class PipeLine(AsyncConsumer):
    def __init__(self, consumer_num=1, only_execute=False):
        super().__init__(consumer_num, only_execute=only_execute)

    def add_job(self, job):
        job.add_pipeline(self)
