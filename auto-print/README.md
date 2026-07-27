# Problem
The turf refreshing process was tedious.

It involved opening 50+ PDFs per regional committee, carefully copying the turf tables from each page, and pasting to Google sheets.

# High-Level Workflow
Use a python script on a folder of turf PDFs to output CSV.

The CSV can then be copy/pasted to excel/sheets to fix misnames, identify duplicates, and sort by priority.

After cleaning up the list in Excel/Sheets, the final result can be pasted to the Turf Tracking tab.

# Setup
1. Install python
  - Windows: Download installer from [https://www.python.org/downloads/](https://www.python.org/downloads/)
  - Mac:
```
brew install python
```
2. Install pymupdf
  - Windows:
```
pip install pymupdf
```

  - Mac:
```
brew install pymupdf
```

# Usage
1. python .\turf-pdf-to-csv.py --dir <path to turf PDF folder>

2. Copy/paste to excel/sheets for further parsing

# Parameters
- `--dir`: Specify directories containing PDFs to parse. Defaults to current working directory if not specified

- `--stdout`: Specify this flag to output to stdout instead of to CSV file
