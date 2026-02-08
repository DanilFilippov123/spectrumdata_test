from fetcher.factory import make_fetcher
from parser.factory import make_parser
from repository.factory import make_page_repository
from task.interface import TaskExecutor
from task.parse_pages import ParsePagesTask


def make_parse_page_task(task_executor: TaskExecutor) -> ParsePagesTask:
    return ParsePagesTask(
        parser=make_parser(),
        fetcher=make_fetcher(),
        task_executor=task_executor,
        page_repository=make_page_repository(),
    )
