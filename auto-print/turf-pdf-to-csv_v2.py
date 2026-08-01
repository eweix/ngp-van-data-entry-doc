# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "ezsheets>=2026.4.28",
#     "pypdf>=6.14.2",
#     "pyperclip>=1.11.0",
# ]
# ///
import re
import logging
import sys
import pyperclip
import csv
import time

import ezsheets
from pypdf import PdfReader
from argparse import ArgumentParser
from pathlib import Path

TIMESTAMP = time.strftime("%Y%m%d-%H%M-%S")


def extract_data(
    p: Path,
    pagelim=3,
):
    """Extract turf data from the pdf

    This function takes in a path and reads the associated pdf.
    The generated pdfs usually store turf information on the first page, so
    to save time the function only reads that page.

    Specific pages can instead be set using the `pages` keyword.
    Setting pages=-1 will instead check EVERY page, which greatly increases
    processing time.

    Args:
        p:      path to the pdf input
        data:  optional list to add turf information to.
        pages:  pages in the pdf to check for turf information.


    Returns:
        data:  list of lists in the form [[full_name, name, location_type, ward,
               list_number, turf_number, num_doors]]
    """
    tr = re.compile(
        r"(?P<code>\d+-\d+)\s*(?P<turf>Turf \d+)\s*\d+\s*(?P<num_doors>\d+)"
    )
    pr = re.compile(
        r"^Turf Packet Summary.*?([a-zA-z\d]*_*[\sa-zA-z]*_*(.*?)(City|C|Village|V|Town|T])?_*(\d+)_*.*)"
    )
    logging.debug(f"{p.name} : extracting text from all pages")
    pagelim = None if pagelim == -1 else pagelim
    data = list()
    for i, page in enumerate(PdfReader(p).pages[:pagelim]):
        text = page.extract_text(extraction_mode="layout")
        # metadata exists only on first page
        if i == 0:
            meta = list(next(pr.finditer(text)).groups())
            assert len(meta) == 4
            # normalize district type
            meta[2] = {
                "City": "C",
                "Town": "T",
                "Village": "V",
                "C": "C",
                "T": "T",
                "V": "V",
            }[meta[2]]
            meta[3] = meta[3].zfill(4)  # left pad ward to 4 digits
        data.extend(meta + list(m.groups()) for m in tr.finditer(text))
        logging.debug(
            f"{p.name} : page {page} - {sum(1 for _ in tr.finditer(text))} matches"
        )
    return data


def update_sheet(url, data):
    """Update google sheet input"""
    logging.debug(f"Spreadsheet url: {url}")
    ss = ezsheets.Spreadsheet(url)
    sheet = ss.Sheet(f"turf_list_{TIMESTAMP}.csv")
    sheet.updateRows(data)
    return


def _parse_args():
    """return arguments and inputs from the argument parser"""
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        nargs="*",
        type=Path,
        default=[Path.cwd()],
        help="Input turf pdf(s).",
    )
    parser.add_argument(
        "-r",
        "--remote",
        type=str,
        default=None,
        help="URL for google spreadsheet to update",
    )
        "-o",
        "--output",
        type=Path,
        help="Output file name. \nDefault: turf_list_YYYYmmdd-HHMM-SS.csv",
        default=Path(f"./turf_list_{TIMESTAMP}.csv"),
    )
    parser.add_argument(
        "-c",
        "--copy",
        action="store_true",
        help="Copy combined turf data output to system clipboard. \nDefault: False",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Send output to stdout instead of to file.\nDefault: false",
    )
    parser.add_argument(
        "--pagelim",
        default=3,
        help="Process up to this page in the pdf.\nDefault: 3",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="Enable verbose output for debugging. Cumulative.",
    )
    args = parser.parse_args()

    if args.verbose == 0:
        level = logging.WARNING
        logging.info("Running script...")
    elif args.verbose == 1:
        level = logging.INFO
        logging.info("Starting script in verbose mode...")
    else:
        level = logging.DEBUG
        logging.info("Starting script in debug mode...")

    logging.basicConfig(level=level)
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    logging.getLogger("ezsheets").setLevel(logging.ERROR)

    # check if stdin is interactive
    # allows users to pipe input into the script
    if not sys.stdin.isatty():
        files = [
            Path(p.rstrip())
            for p in sys.stdin
            if not Path(p.rstrip()).is_dir() and p.rstrip().endswith(".pdf")
        ]
        for d in (Path(d.rstrip()) for d in sys.stdin if Path(d.rstrip()).is_dir()):
            files.extend(d.glob("*.pdf"))
    elif args.input:
        files = [p for p in args.input if not p.is_dir() and p.suffix == ".pdf"]
        for d in (d for d in args.input if d.is_dir()):
            files.extend(d.glob("*.pdf"))

    if len(files) == 0:
        parser.print_help()
        sys.exit(0)

    logging.info(f"Got {len(files)} input files")
    for file in files:
        logging.debug(f"\t{str(file)}")

    if not args.stdout:
        logging.debug(f"output: {str(args.output)}")
    else:
        logging.debug("output: stdout")

    return args, files


def main():
    args, files = _parse_args()
    logging.info("exporting turf data...")
    data = [
        [
            "region_name_raw",
            "civil_district_name",
            "civil_district_type",
            "ward_number",
            "list_number",
            "turf_number",
            "door_count",
        ]
    ]
    for f in files:
        data.extend(extract_data(f, pagelim=args.pagelim))
    if args.stdout:
        csv.writer(sys.stdout).writerows(data)
    else:
        with open(args.output, "w") as output:
            csv.writer(output).writerows(data)
    if args.copy:
        pyperclip.copy(data)
    if args.remote:
        update_sheet(args.remote, data)


if __name__ == "__main__":
    main()
