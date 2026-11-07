from pathlib import Path

from converters import TARGETS, validate

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_validate_ok_csv_json():
    error = validate(
        "csv",
        "json",
        str(SAMPLES / "people.csv"),
        str(SAMPLES / "out.json"),
    )
    assert error is None


def test_validate_missing_from_format():
    error = validate("", "json", str(SAMPLES / "people.csv"), "out.json")
    assert error == "Error: choose a From format"


def test_validate_missing_input_file():
    error = validate("csv", "json", None, "out.json")
    assert error == "Error: choose an input file"


def test_validate_unsupported_pair():
    error = validate(
        "csv",
        "odt",
        str(SAMPLES / "people.csv"),
        "out.odt",
    )
    assert error == "Error: cannot convert csv to odt"


def test_validate_wrong_extension():
    error = validate(
        "json",
        "csv",
        str(SAMPLES / "people.csv"),
        "out.csv",
    )
    assert "input file is .csv" in error


def test_available_targets_matrix():
    assert TARGETS["csv"] == ("json",)
    assert TARGETS["json"] == ("csv",)
    assert "txt" in TARGETS["docx"]
    assert "odt" in TARGETS["docx"]
    assert TARGETS["txt"] == ("docx",)
    assert TARGETS["odt"] == ("docx",)
