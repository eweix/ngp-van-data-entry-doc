import re
import sys
from pathlib import Path
import pymupdf
import csv
import argparse
import time

def turf_pdf_to_csv(target_dir_list, is_stdout):
    map_region_pdf_list = []
    for target_dir in target_dir_list:
        map_region_pdf_list.extend(get_child_pdf(target_dir))

    # Parse first couple of pages of map region PDFs
    output_list = []
    for map_region_pdf in map_region_pdf_list:
        map_region_doc = pymupdf.open(map_region_pdf.resolve())

        # I hope we don't have any single ward with more than 3 pages of turfs
        for page_num, page in enumerate(map_region_doc[:3]):
            map_region_page = page.get_text()

            map_region_page_lines = map_region_page.splitlines()

            if (page_num == 0) and map_region_page_lines:
                # Get the map region name from first page
                turf_packet_summary_line = map_region_page_lines[0]
                map_region_name_raw = turf_packet_summary_line[len("Turf Packet Summary - "):]
                if map_region_name_raw == "":
                    break

                # Use regex for region names misnamed with multiple underscores
                region_name_split = re.split(r'_+', map_region_name_raw)

                # Protect against poorly named map regions
                if len(region_name_split) > 2:
                    district_types = {
                        "City" : "C",
                        "Town" : "T",
                        "Village" : "V",
                        "C" : "C",
                        "T" : "T",
                        "V" : "V",
                        "Vge" : "V",
                    }
                    civil_district = region_name_split[2]
                    for district_type_full in district_types.keys():
                        civil_district_lower = civil_district.lower()
                        district_type_full_lower = district_type_full.lower()
                        if civil_district_lower.endswith(district_type_full_lower):
                            civil_district_name = civil_district[:-len(district_type_full_lower)]
                            civil_district_type = district_types[district_type_full]
                            break
                    else:
                        # Just put it in the name column if it's really misnamed
                        civil_district_name = civil_district
                        civil_district_type = ""

                else:
                    civil_district_name = ""
                    civil_district_type = ""

                if len(region_name_split) > 3:
                    ward_number = region_name_split[3].zfill(4)
                else:
                    ward_number = ""

            # Go through the rest of the lines for the
            # list number, turf number, and door count
            for line_num, line in enumerate(map_region_page_lines):
                if not is_list_number(line):
                    continue

                list_number = line
                if len(map_region_page_lines) > line_num + 1:
                    turf_number = map_region_page_lines[line_num + 1]
                else:
                    turf_number = ""
                
                if len(map_region_page_lines) > line_num + 3:
                    door_count = map_region_page_lines[line_num + 3]
                else:
                    door_count = ""

                output_list.append((map_region_name_raw,
                                    civil_district_name, 
                                    civil_district_type,
                                    ward_number,
                                    list_number, 
                                    turf_number,
                                    door_count))

    # Write output
    timestamp = time.strftime(("%Y%m%d-%H%M-%S"))
    output_filename = "turf_list_" + timestamp + ".csv"
    if is_stdout:
        stdout_writer = csv.writer(sys.stdout)
        stdout_writer.writerow([
            "region_name_raw", 
            "civil_district_name", 
            "civil_district_type",
            "ward_number", 
            "list_number", 
            "turf_number", 
            "door_count"])
        stdout_writer.writerows(output_list)
    else:
        with open(output_filename, newline = "", mode="w") as csvfile:
            csvfile_writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            csvfile_writer.writerow([
                "region_name_raw", 
                "civil_district_name",
                "civil_district_type",
                "ward_number",
                "list_number",
                "turf_number",
                "door_count"])
            csvfile_writer.writerows(output_list)

        print(f"Output: {Path(output_filename).resolve()}")

    return

def get_child_pdf(target_dir):
    pdf_list = []
    for item in target_dir.iterdir():
        if not item.is_file():
            continue
        if item.suffix != ".pdf":
            continue

        pdf_list.append(item)

    return pdf_list

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
        nargs="*",
        type=Path,
        default=None,
        help="Specify directories containing PDFs to parse. Default: cwd",
    )

    parser.add_argument(
        "--dir",
        nargs="*",
        type=Path,
        default=None,
        help="Specify directories containing PDFs to parse. Default: cwd",
        dest="dir_flag",
    )

    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Output CSV to stdout instead of a file"
    )

    args = parser.parse_args()

    target_dir_list = args.dir or args.dir_flag or [Path.cwd()]
    is_stdout = args.stdout or False

    turf_pdf_to_csv(target_dir_list, is_stdout)

if __name__ == "__main__":
    main()
