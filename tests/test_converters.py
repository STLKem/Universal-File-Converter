import json
from pathlib import Path

import pytest

from converters import convert, csv_to_json, json_to_csv

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_csv_to_json_keeps_polish_and_empty_notes(tmp_path):
    target = tmp_path / "people.json"
    csv_to_json(str(SAMPLES / "people.csv"), str(target))

    data = json.loads(target.read_text(encoding="utf-8"))
    assert data[0]["name"] == "Anna Kowalska"
    assert "Gdańsk" in data[0]["city"]
    assert data[1]["name"] == "Łukasz Żółć"
    assert data[1]["notes"] == ""


def test_json_to_csv_roundtrip_headers(tmp_path):
    target = tmp_path / "people.csv"
    json_to_csv(str(SAMPLES / "people.json"), str(target))

    lines = target.read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("id,name,email")
    assert "Łukasz Żółć" in target.read_text(encoding="utf-8")
    assert "Wrocław" in target.read_text(encoding="utf-8")


def test_convert_csv_json_via_registry(tmp_path):
    target = tmp_path / "out.json"
    convert("csv", "json", str(SAMPLES / "people.csv"), str(target))
    assert target.exists()
    assert "Preferuje e-mail" in target.read_text(encoding="utf-8")


def test_broken_json_raises_clear_error(tmp_path):
    target = tmp_path / "out.csv"
    with pytest.raises(ValueError, match="Broken JSON file"):
        convert("json", "csv", str(SAMPLES / "broken.json"), str(target))


def test_broken_csv_missing_header_raises(tmp_path):
    source = tmp_path / "broken.csv"
    source.write_text("", encoding="utf-8")
    target = tmp_path / "out.json"
    with pytest.raises(ValueError, match="Broken CSV file"):
        convert("csv", "json", str(source), str(target))


def test_txt_to_docx_and_back(tmp_path):
    docx_path = tmp_path / "people.docx"
    txt_path = tmp_path / "people_back.txt"

    convert("txt", "docx", str(SAMPLES / "people.txt"), str(docx_path))
    assert docx_path.exists()

    convert("docx", "txt", str(docx_path), str(txt_path))
    text = txt_path.read_text(encoding="utf-8")
    assert "Anna Kowalska" in text
    assert "Łukasz" in text or "Kowalska" in text


def test_docx_to_odt(tmp_path):
    odt_path = tmp_path / "people.odt"
    convert("docx", "odt", str(SAMPLES / "people.docx"), str(odt_path))
    assert odt_path.exists()
    assert odt_path.stat().st_size > 0


def test_odt_to_docx(tmp_path):
    docx_path = tmp_path / "from_odt.docx"
    convert("odt", "docx", str(SAMPLES / "people.odt"), str(docx_path))
    assert docx_path.exists()
    assert docx_path.stat().st_size > 0
