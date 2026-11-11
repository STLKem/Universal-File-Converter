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

PANDOC_PAIRS = {
    ("docx", "txt"),
    ("txt", "docx"),
    ("docx", "odt"),
    ("odt", "docx"),
}


def csv_to_json(source, target):
    with open(source, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        if reader.fieldnames is None:
            raise ValueError("Broken CSV file: missing header row")
        data = list(reader)

    with open(target, mode="w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, indent=4, ensure_ascii=False)


def json_to_csv(source, target):
    with open(source, mode="r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    if not isinstance(data, list) or not data:
        raise ValueError("Broken JSON file: expected a non-empty list of objects")
    if not isinstance(data[0], dict):
        raise ValueError("Broken JSON file: expected objects with fields")

    with open(target, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def docx_to_txt(source, target):
    pypandoc.convert_file(source, "plain", outputfile=target)


def txt_to_docx(source, target):
    pypandoc.convert_file(source, "docx", format="markdown", outputfile=target)


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


def check_pandoc():
    try:
        pypandoc.get_pandoc_path()
    except OSError as e:
        raise RuntimeError(
            "Pandoc not found. Install Pandoc or run: "
            "pip install pypandoc_binary"
        ) from e


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
            f"Error: output file is .{target_ext or 'missing'}, "
            f"but To is set to {target_format}"
        )

    if (source_format, target_format) in PANDOC_PAIRS:
        try:
            check_pandoc()
        except RuntimeError as e:
            return str(e)

    return None


def convert(source_format, target_format, source_path, target_path):
    if (source_format, target_format) in PANDOC_PAIRS:
        check_pandoc()

    try:
        CONVERTERS[(source_format, target_format)](source_path, target_path)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Broken JSON file: {e}. Fix the file or choose another one."
        ) from e
    except csv.Error as e:
        raise ValueError(
            f"Broken CSV file: {e}. Fix the file or choose another one."
        ) from e
    except UnicodeDecodeError as e:
        raise ValueError(
            f"Invalid file encoding: {e}. Please use UTF-8."
        ) from e
    except OSError as e:
        message = str(e)
        if "pandoc" in message.lower():
            raise RuntimeError(
                "Pandoc not found. Install Pandoc or run: "
                "pip install pypandoc_binary"
            ) from e
        raise ValueError(
            f"Unreadable or damaged file: {e}. "
            "Check that the input file is valid."
        ) from e
    except RuntimeError:
        raise
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(
            f"Unsupported or damaged file content: {e}. "
            "Check that the input file is valid."
        ) from e
