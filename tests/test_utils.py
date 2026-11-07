from utils import default_output_name, ensure_extension, shorten_path


def test_shorten_path_keeps_short_value():
    assert shorten_path("people.csv") == "people.csv"


def test_shorten_path_adds_ellipsis():
    long_path = "D:/Universal-File-Converter/samples/people.csv"
    short = shorten_path(long_path, max_chars=20)
    assert short.startswith("...")
    assert short.endswith("people.csv")
    assert len(short) == 20


def test_default_output_name_from_source():
    assert default_output_name(r"D:\data\people.csv", "json") == "people.json"


def test_default_output_name_without_source():
    assert default_output_name(None, "csv") == "output.csv"


def test_ensure_extension_adds_missing_suffix():
    assert ensure_extension(r"D:\out\people", "json").endswith("people.json")


def test_ensure_extension_fixes_wrong_suffix():
    assert ensure_extension(r"D:\out\people.txt", "csv").endswith("people.csv")
