from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

APP_LOG = LOG_DIR / "app.log"
TEST_LOG = LOG_DIR / "tests.log"


def _write(path: Path, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with path.open("a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")


def write_app_log(message: str) -> None:
    _write(APP_LOG, message)


def write_test_log(message: str) -> None:
    _write(TEST_LOG, message)
