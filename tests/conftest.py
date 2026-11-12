import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app_logger import write_test_log


def pytest_sessionstart(session):
    write_test_log("===== TEST SESSION START =====")


def pytest_runtest_logreport(report):
    if report.when != "call":
        return

    if report.passed:
        status = "PASSED"
    elif report.failed:
        status = "FAILED"
    elif report.skipped:
        status = "SKIPPED"
    else:
        status = report.outcome.upper()

    write_test_log(f"{status}: {report.nodeid}")
    if report.failed and report.longrepr:
        write_test_log(f"  details: {report.longrepr}")


def pytest_sessionfinish(session, exitstatus):
    write_test_log(
        f"===== TEST SESSION END (exitstatus={exitstatus}) ====="
    )
