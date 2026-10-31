import html

import pytest
from pytest_html import extras


def pytest_html_report_title(report):
    report.title = "FMS Automation Report (Demo, mock server)"


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>What it checks</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{html.escape(getattr(report, 'description', '-'))}</td>")


@pytest.fixture()
def steps(request):
    request.node._steps = []

    def add(text):
        request.node._steps.append(text)

    return add


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    doc = " ".join((item.function.__doc__ or "-").split())
    report.description = doc
    if report.when == "call":
        steps = getattr(item, "_steps", [])
        if steps:
            rows = "".join(f"<li>{html.escape(s)}</li>" for s in steps)
            box = f"<div><b>How it ran:</b><ol>{rows}</ol></div>"
            report.extras = getattr(report, "extras", []) + [extras.html(box)]