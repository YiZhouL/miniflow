import asyncio

from src import miniflow
from src.miniflow import Job


@miniflow.register_func(5)
async def do_something(self: Job):
    print(self.__str__())


new_scheduler = miniflow.create_new_scheduler()


@new_scheduler(5)
@miniflow.register_job(3)
class DemonJob(Job):
    async def _run(self):
        print(self.__str__())


@miniflow.register_func(60)
async def do(self: Job):
    await asyncio.sleep(10)
    miniflow.stop()


if __name__ == "__main__":
    miniflow.start()
