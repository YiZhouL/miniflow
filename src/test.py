from src import miniflow
from src.miniflow import Job


@miniflow.register_func(5)
async def do_something(self: Job):
    print(self.__str__())


@miniflow.register_job(3)
class DemonJob(Job):
    async def _run(self):
        print(self.__str__())


if __name__ == "__main__":
    miniflow.start()


