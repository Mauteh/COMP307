#!/usr/bin/env python3
"""Import and validate CRF variable definitions from a CSV file."""

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

REQUIRED_COLUMNS = {"variable_name", "description", "data_type"}
SUPPORTED_TYPES = {"string", "integer", "decimal", "date", "boolean"}


@dataclass
class ImportResult:
    rows: List[dict]
    errors: List[str]


def validate_csv(path: Path) -> ImportResult:
    """Read a CRF CSV without modifying it and report row-level validation errors."""
    errors = []
    rows = []
    try:
        with path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                return ImportResult([], ["The CSV file is empty or has no header row."])

            normalized = [name.strip() for name in reader.fieldnames if name]
            missing = REQUIRED_COLUMNS - set(normalized)
            if missing:
                return ImportResult([], [
                    "Missing required column(s): " + ", ".join(sorted(missing))
                ])

            for line_number, raw in enumerate(reader, start=2):
                # Normalize headers and cell whitespace, but preserve the source file.
                row = {(key or "").strip(): (value or "").strip()
                       for key, value in raw.items()}
                name = row.get("variable_name", "")
                description = row.get("description", "")
                data_type = row.get("data_type", "").lower()

                row_errors = []
                if not name:
                    row_errors.append("variable_name is required")
                if not description:
                    row_errors.append("description is required")
                if not data_type:
                    row_errors.append("data_type is required")
                elif data_type not in SUPPORTED_TYPES:
                    row_errors.append(
                        f"unsupported data_type '{data_type}' "
                        f"(supported: {', '.join(sorted(SUPPORTED_TYPES))})"
                    )

                if row_errors:
                    errors.append(f"Row {line_number}: " + "; ".join(row_errors))
                else:
                    rows.append({
                        "variable_name": name,
                        "description": description,
                        "data_type": data_type,
                    })

    except FileNotFoundError:
        return ImportResult([], [f"File not found: {path}"])
    except UnicodeDecodeError:
        return ImportResult([], ["Unable to read file: expected UTF-8 encoded CSV."])
    except csv.Error as exc:
        return ImportResult([], [f"Malformed CSV: {exc}"])
    except OSError as exc:
        return ImportResult([], [f"Unable to read file: {exc}"])

    return ImportResult(rows, errors)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Import and validate CRF variable definitions from CSV."
    )
    parser.add_argument("csv_file", help="Path to input CSV file")
    args = parser.parse_args(argv)

    result = validate_csv(Path(args.csv_file))
    if result.errors:
        print("Validation completed with issues:")
        for error in result.errors:
            print(f"- {error}")
    print(f"Successfully imported variables: {len(result.rows)}")

    if result.errors:
        print("Import status: REVIEW REQUIRED (invalid rows were not imported).")
        return 1

    print("Import status: SUCCESS")
    for row in result.rows:
        print(f"- {row['variable_name']} ({row['data_type']}): {row['description']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
