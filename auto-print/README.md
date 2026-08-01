# Problem
The turf refreshing process was tedious.

It involved opening 50+ PDFs per regional committee, carefully copying the turf tables from each page, and pasting to Google sheets.

# High-Level Workflow
Use a python script on a folder of turf PDFs to output CSV.

The CSV can then be copy/pasted to excel/sheets to fix misnames, identify duplicates, and sort by priority.

After cleaning up the list in Excel/Sheets, the final result can be pasted to the Turf Tracking tab.

# turf-pdf-to-csv.py
## Setup
1. Install python 3.14 or later (*I think I'm using something from 3.9, but I have 3.14 installed*)
    - Windows: Download python 3.14 or later from [https://www.python.org/downloads/](https://www.python.org/downloads/)
    - Mac: `brew install python`
2. Install pymupdf
    - Windows: `pip install pymupdf`
    - Mac: `brew install pymupdf`

Alternatively, installation and usage can be managed using [uv][uv]. The script
works with python version 3.9 or later.

```sh
uv run turf-pdf-to-csv.py --dir <path to turf PDF folder>
```

[uv]: https://github.com/astral-sh/uv

## Usage
1. Run python script
    - Windows: `py .\turf-pdf-to-csv.py --dir <path to turf PDF folder>`
    - Mac: `python3 .\turf-pdf-to-csv.py --dir <path to turf PDF folder>`

2. A csv file will be created named `turf_list_<timestamp>.csv`

3. Copy/paste CSV to the `format_for_turf_tracker.xlsx` spreadsheet for further parsing

## Parameters
- `--dir`: Specify one or more directories containing PDFs to parse. Defaults to current working directory if not specified

- `--stdout`: Set this flag to write to stdout instead of to a CSV file

# format_for_tuf_tracker.xlst

1. Double-click the xlst to open a copy of the template
2. Paste the csv output to the first table in the `Fixup` tab
3. On the `Fixup` tab, fix any map region names:
    - Fill out any missing civil district type abbreviations (C, V, T...) in the `civil_district_type` column
    - Use the `Misname` tab to correct any civil district names
        - ex. `StevensPoint` to `Stevens Point` (*not a misname, but I didn't automate adding back whitespace...*)
        - ex. `StevensPt` to `Stevens Point`
    - If anything looks really messed up, then you should audit the map region in votebuilder
        - ex. check that the map region Home District criterion is pointing at the right ward
    - (Optional) Use the `duplicate_finder` column to find duplicates. (You should delete one of the duplicates in votebuilder.)
4. Add ward priority to the `Prio` tab (*this could be automated...*):
    1. Open your regional committe's Canvass and Turf Tracker
    2. Open the Ward Tracking tab
    3. Copy the priority and ward name column
    4. Paste to the `Prio` tab
5. You now have the final, unsorted result in the 3rd table on the `Fixup` tab
    - If there are any missing priorities still, go back to step #3
6. Copy the unsorted table. Paste the values to the `Sort` tab and sort
7. Copy/paste the final, sorted result to the `GOTV Turf Tracking Tab` in Sheets
8. (Optional) Use the `Prio` tab's `turf_count` column to fill out the `# of Turf Packets` on the `Ward Tracking` tab of the Canvass and Turf Tracker

# AI Disclosure
- AI was used to research python documentation and best practices
- Github copilot was used for inline completions and next edit suggestions
- Agentic coding tools were NOT used
