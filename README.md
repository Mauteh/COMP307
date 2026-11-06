# CRF Variable Mapper – CSV Import Prototype

## Feature
This prototype implements Assignment 1 User Story 1 (Import CRF Variables) and the related validation checks in User Story 5.

## Requirements
- Python 3.9 or newer
- No third-party packages are required to run the application.
- `pytest` is required only to run the automated tests.

## Run
From this directory:

```bash
python crf_mapper.py sample_crf_variables.csv
```

Try the invalid example:

```bash
python crf_mapper.py sample_invalid_variables.csv
```

The application prints validation messages and the count of successfully imported rows. It exits with status code `0` on success and `1` when validation issues exist.

## Test
Install pytest if needed, then run:

```bash
python -m pip install pytest
python -m pytest -v
```

The tests cover successful import, missing columns, invalid row values, and preservation of the original input file.

## CSV format
The header must contain `variable_name`, `description`, and `data_type`.
Supported data types are: `string`, `integer`, `decimal`, `date`, and `boolean`.

## Design boundaries
The prototype validates and imports rows only. It does not yet connect to a CDASH dictionary, generate mapping suggestions, or export approved mappings. Invalid rows are reported and excluded from the imported result; the original file is never rewritten.
