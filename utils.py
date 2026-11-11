from pathlib import Path


def shorten_path(path, max_chars=36):
    if len(path) <= max_chars:
        return path
    return "..." + path[-(max_chars - 3):]


def default_output_name(source_path, target_format):
    if source_path:
        return f"{Path(source_path).stem}.{target_format}"
    return f"output.{target_format}"


def ensure_extension(path, target_format):
    result = Path(path)
    if result.suffix.lower().lstrip(".") != target_format:
        result = result.with_suffix(f".{target_format}")
    return str(result)
