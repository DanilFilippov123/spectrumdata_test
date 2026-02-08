from spectrumdata_test.fetcher.factory import make_fetcher
from spectrumdata_test.parser.factory import make_parser
from spectrumdata_test.repository.factory import make_page_repository
from spectrumdata_test.task.interface import TaskExecutor
from spectrumdata_test.task.parse_pages import ParsePagesTask


def make_parse_page_task(task_executor: TaskExecutor) -> ParsePagesTask:
    return ParsePagesTask(
        parser=make_parser(),
        fetcher=make_fetcher(),
        task_executor=task_executor,
        page_repository=make_page_repository(),
    )
