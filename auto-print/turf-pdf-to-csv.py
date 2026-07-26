import os
import os.path
import sys
from pathlib import Path
# import subprocess
import pymupdf

def turf_pdf_to_csv():
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

    cwd = Path(__file__).parent.resolve()
    print(cwd)

    pdf_list = []

    for item in cwd.iterdir():
        if not item.is_file():
            continue
        if item.suffix != ".pdf":
            continue

        pdf_list.append(item)

    print(pdf_list)

    # for pdf in pdf_list:
    #     pdf_path = pdf.resolve()
    #     subprocess.call(['pdftotext', pdf_path])

    for pdf_path in pdf_list:
        pdf_obj = pymupdf.open(pdf_path.resolve())

        # page_num = 0 # this is weird I don't know the python way to do this

        # I hope we don't have any single ward with more than 3 pages of turfs
        for page in pdf_obj[:3]:
            text = page.get_text()
            print(text)

            # page_num += 1
            # if page_num > 2:
            #     break




if __name__ == "__main__":
    turf_pdf_to_csv()
