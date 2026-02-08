import asyncio
from asyncio import Queue
from uuid import UUID, uuid4

from loguru import logger

from spectrumdata_test.task.error import ParsePageError
from spectrumdata_test.task.factory import make_parse_page_task
from spectrumdata_test.task.interface import TaskExecutor


async def parse_task_executor(queue: Queue, task_executor: TaskExecutor) -> None:
    logger.debug("started worker")
    while True:
        url, depth = await queue.get()
        logger.debug(f"get {url}")
        task = make_parse_page_task(task_executor)
        try:
            await task.execute(url, depth)
        except ParsePageError:
            logger.exception("failed to parse page")
        except Exception:
            logger.exception("Fatal error")
        finally:
            queue.task_done()


class AsyncioTaskExecutor(TaskExecutor):
    def __init__(self, queue: Queue, max_depth: int = 0) -> None:
        self._queue = queue
        self._max_depth = max_depth

    async def add_task(self, url: str, depth: int) -> None:
        if depth > self._max_depth:
            return
        await self._queue.put((url, depth))


TASKS = {}

class AsyncioTaskQueue:
    async def parse_task_scheduler(self) -> None:
        await self._queue.join()
        for worker in self.workers:
            logger.debug(f"Stopping task {self._uuid} worker")
            worker.cancel()
        del TASKS[self._uuid]

    def __init__(self, url: str, depth: int, max_concurrency: int) -> None:
        self._uuid = uuid4()
        self._queue = Queue()
        self.workers = [
            asyncio.create_task(
                parse_task_executor(
                    queue=self._queue,
                    task_executor=AsyncioTaskExecutor(
                        queue=self._queue, max_depth=depth
                    ),
                )
            )
            for _ in range(max_concurrency)
        ]
        logger.info(f"Starting task {self._uuid} - {len(self.workers)} workers")
        self._queue.put_nowait((url, 0))
        asyncio.create_task(self.parse_task_scheduler())
        TASKS[self._uuid] = self

    @property
    def uuid(self) -> UUID:
        return self._uuid
