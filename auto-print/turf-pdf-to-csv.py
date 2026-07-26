# import os
# import os.path
import sys
from pathlib import Path

# import subprocess
import pymupdf
import csv
import argparse


def turf_pdf_to_csv(target_dir):
    # cwd = os.getcwd()
    # files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]
    #
    # for file in files:
    #     print(file)
    #
    # for item in os.listdir(cwd):
    #     if not os.path.isfile(os.path.join(cwd, item)):
    #         continue
    #     if not os.path.splitext

    # target_dir = Path(__file__).parent.resolve()
    # print(target_dir)

    map_region_pdf_list = []

    for item in target_dir.iterdir():
        if not item.is_file():
            continue
        if item.suffix != ".pdf":
            continue

        map_region_pdf_list.append(item)

    # print(map_region_pdf_list)

    # for pdf in pdf_list:
    #     pdf_path = pdf.resolve()
    #     subprocess.call(['pdftotext', pdf_path])

    output_list = []

    for map_region_pdf in map_region_pdf_list:
        map_region_doc = pymupdf.open(map_region_pdf.resolve())

        # page_num = 0 # this is weird I don't know the python way to do this

        # I hope we don't have any single ward with more than 3 pages of turfs
        for page in map_region_doc[:3]:
            map_region_page = page.get_text()
            # print(map_region_page)

            map_region_page_lines = map_region_page.splitlines()

            for line_num, line in enumerate(map_region_page_lines):
                if not is_list_number(line):
                    continue

                # print(line)

                list_number = line
                turf_number = map_region_page_lines[line_num + 1]
                door_count = map_region_page_lines[line_num + 3]

                output_list.append((list_number, turf_number, door_count))

    stdout_writer = csv.writer(sys.stdout)
    stdout_writer.writerow(["list_number", "turf_number", "door_count"])
    stdout_writer.writerows(output_list)

    return


def is_list_number(line):
    return (
        len(line) == 14 and line[8] == "-" and line[:8].isdigit() and line[9:].isdigit()
    )


def main():
    parser = argparse.ArgumentParser(
        prog="turf_pdf_to_csv", description="Turn turf PDFs into CSV"
    )
    parser.add_argument(
        "dir",
        nargs="?",
        type=Path,
        default=None,
        help="Specify a directory containing PDFs to parse. Default: cwd",
    )

    parser.add_argument(
        "--dir",
        nargs="?",
        type=Path,
        default=None,
        help="Specify a directory containing PDFs to parse. Default: cwd",
        dest="dir_flag",
    )

    args = parser.parse_args()

    target_dir = args.dir or args.dir_flag or Path.cwd()

    turf_pdf_to_csv(target_dir)


if __name__ == "__main__":
    # turf_pdf_to_csv()
    main()
