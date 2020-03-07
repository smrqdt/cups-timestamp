#! /usr/bin/env python3

import locale
import logging
import os
import os.path
import sys
import typing
from datetime import datetime
from io import BytesIO

import cups
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import RectangleObject
from reportlab.lib import colors, pagesizes, units
from reportlab.pdfgen import canvas

logging.basicConfig(filename="process.log", level=logging.INFO)
locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

# output directory to place timestamped PDF in
# OUTPUT_DIR = "/opt/ecodms/workdir/scaninput/printinput"
OUTPUT_DIR = "/tmp"

# pass timestamped PDF to the following printer
# printing will be skipped if PRINTER_NAME is empty
PRINTER_NAME = "PDF"

# delete original file aber stamping?
DELETE_INPUT_FILE = False

# set file mode (permissions) for created file
# default is read and write permissions for all users
OUTPUT_CHMOD = 0o666


def main():
    # cups-pdf will pass the following arguments
    input_filename = sys.argv[1]  # path to pdf file
    user_exec = sys.argv[2]  # user to which CUPS-PDF attached the print job
    user_passed = sys.argv[3]  # user name which was passed with the print job
    logging.info(f"Filename: %s", input_filename)
    logging.info(f"user_exec: %s", user_exec)
    logging.info(f"user_passed: %s", user_passed)

    output_filename = os.path.join(OUTPUT_DIR,
                                   os.path.basename(input_filename))

    with open(input_filename, "rb") as input_pdf:
        with open(output_filename, "wb") as output_pdf:
            add_stamp(input_pdf, output_pdf, user_passed)
    hardcopy(output_filename)

    delete_file(input_filename)

    os.chmod(output_filename, OUTPUT_CHMOD)


def add_stamp(input_pdf: typing.BinaryIO, output_pdf: typing.BinaryIO,
              user: str):
    """apply stamp to first page of the pdf

    the timestamp will be placed in the top left corner"""
    out = PdfFileWriter()
    input_reader = PdfFileReader(input_pdf)

    page1 = input_reader.getPage(0)
    stamp_pdf = create_stamp(user, page1.mediaBox)
    stamp_reader = PdfFileReader(stamp_pdf)
    stamp = stamp_reader.getPage(0)
    page1.mergePage(stamp)
    for page in input_reader.pages:
        out.addPage(page)

    out.write(output_pdf)


def create_stamp(user: str, media_box: RectangleObject):
    """generate stamp using reportlab"""
    buffer = BytesIO()
    stamp = canvas.Canvas(buffer, pagesize=pagesizes.A4)
    x_left, y_top = media_box.upperLeft
    stamp.translate(x_left + 0.7 * units.cm,
                    y_top.as_numeric() - 0.7 * units.cm)
    text = stamp.beginText(0, 0)
    text.setFont("Courier-Bold", 14)
    text.setFillColor(colors.mediumblue)
    text.textOut("Archiviert: ")
    text.setFillColor(colors.crimson)
    text.textOut(datetime.now().strftime('%a., %d. %b %Y'))
    text.setFont("Courier", 14)
    text.setFillColor(colors.darkorange)
    text.textOut(f" [{user}]")
    stamp.drawText(text)
    stamp.showPage()
    stamp.save()

    buffer.seek(0)
    return buffer


def hardcopy(filename: str):
    """pass timestamped PDF to real printer for hardcopy

    to skip this set PRINTER_NAME to an False/empty string"""
    if not PRINTER_NAME:
        return
    conn = cups.Connection()
    logging.info("Passing %s to printer for hardcopy", filename)
    conn.printFile(PRINTER_NAME, filename, f"Timestamped {filename}",
                   options={})


def delete_file(filename: str):
    if DELETE_INPUT_FILE:
        logging.info("deleting input file")
        os.remove(filename)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.fatal(e)
        print(e)
        sys.exit(1)
