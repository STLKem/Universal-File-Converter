from pathlib import Path
import csv
import json

import pypandoc

TARGETS = {
    "csv": ("json",),
    "json": ("csv",),
    "docx": ("txt", "odt"),
    "txt": ("docx",),
    "odt": ("docx",),
}


def csv_to_json(source, target):
    with open(source, mode="r", newline="", encoding="utf-8") as csvfile:
        data = list(csv.DictReader(csvfile))

    with open(target, mode="w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4)


def json_to_csv(source, target):
    with open(source, mode="r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    with open(target, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def docx_to_txt(source, target):
    pypandoc.convert_file(source, "plain", outputfile=target)


def txt_to_docx(source, target):
    pypandoc.convert_file(source, "docx", format="plain", outputfile=target)


def docx_to_odt(source, target):
    pypandoc.convert_file(source, "odt", outputfile=target)


def odt_to_docx(source, target):
    pypandoc.convert_file(source, "docx", outputfile=target)


CONVERTERS = {
    ("csv", "json"): csv_to_json,
    ("json", "csv"): json_to_csv,
    ("docx", "txt"): docx_to_txt,
    ("txt", "docx"): txt_to_docx,
    ("docx", "odt"): docx_to_odt,
    ("odt", "docx"): odt_to_docx,
}


def validate(source_format, target_format, source_path, target_path):
    if not source_format:
        return "Error: choose a From format"
    if not target_format:
        return "Error: choose a To format"
    if source_format not in TARGETS:
        return f"Error: unknown From format '{source_format}'"
    if target_format not in TARGETS[source_format]:
        return f"Error: cannot convert {source_format} to {target_format}"

    if not source_path:
        return "Error: choose an input file"
    if not target_path:
        return "Error: choose an output path"

    source = Path(source_path)
    target = Path(target_path)

    if not source.is_file():
        return f"Error: input file not found: {source}"

    source_ext = source.suffix.lower().lstrip(".")
    target_ext = target.suffix.lower().lstrip(".")

    if source_ext != source_format:
        return (
            f"Error: input file is .{source_ext}, but From is set to {source_format}"
        )
    if target_ext != target_format:
        return (
            f"Error: output file is .{target_ext or '(no extension)'}, "
            f"but To is set to {target_format}"
        )

    return None


def convert(source_format, target_format, source_path, target_path):
    CONVERTERS[(source_format, target_format)](source_path, target_path)
