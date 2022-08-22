import enum


class ProcessStatus(enum.Enum):
    CREATED = "已创建"
    STARTED = "正在运行"
    PAUSED = "已暂停"
    STOP = "已停止"


class SimpleProcess:
    num = 0

    def __init__(self):
        self._process_num = self.num
        self.__class__.num += 1
        self._process_status = ProcessStatus.CREATED
        self.start()

    def start(self):
        if self._process_status in [ProcessStatus.CREATED, ProcessStatus.PAUSED]:
            self._process_status = ProcessStatus.STARTED

    @property
    def started(self):
        return self._process_status == ProcessStatus.STARTED

    def stop(self):
        if self._process_status in [ProcessStatus.STARTED, ProcessStatus.PAUSED]:
            self._process_status = ProcessStatus.STOP

    @property
    def stopped(self):
        return self._process_status == ProcessStatus.STOP

    def pause(self):
        if self._process_status == ProcessStatus.STARTED:
            self._process_status = ProcessStatus.PAUSED

    @property
    def paused(self):
        return self._process_status == ProcessStatus.PAUSED

    def __str__(self):
        return "<{}-{}>{}".format(self.__class__.__name__, self._process_num, self._process_status.value)
