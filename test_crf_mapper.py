import csv
from pathlib import Path
from crf_mapper import validate_csv


def write_csv(path: Path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def test_valid_csv_imports_all_rows(tmp_path):
    path = tmp_path / "valid.csv"
    write_csv(path, ["variable_name", "description", "data_type"], [
        ["AGE", "Participant age in years", "integer"],
        ["SEX", "Participant sex", "string"],
    ])
    result = validate_csv(path)
    assert len(result.rows) == 2
    assert result.errors == []


def test_missing_required_column_is_rejected(tmp_path):
    path = tmp_path / "missing.csv"
    write_csv(path, ["variable_name", "description"], [["AGE", "Age"]])
    result = validate_csv(path)
    assert result.rows == []
    assert "Missing required column" in result.errors[0]


def test_invalid_row_is_reported_and_not_imported(tmp_path):
    path = tmp_path / "invalid.csv"
    write_csv(path, ["variable_name", "description", "data_type"], [
        ["", "Missing name", "integer"],
        ["VISIT", "Visit date", "timestamp"],
    ])
    result = validate_csv(path)
    assert result.rows == []
    assert len(result.errors) == 2
    assert "variable_name is required" in result.errors[0]
    assert "unsupported data_type" in result.errors[1]


def test_source_file_is_not_modified(tmp_path):
    path = tmp_path / "preserve.csv"
    original = (
        "variable_name,description,data_type\n"
        "WEIGHT,Body weight,decimal\n"
    )
    path.write_text(original, encoding="utf-8")
    before = path.read_bytes()
    validate_csv(path)
    after = path.read_bytes()
    assert before == after
