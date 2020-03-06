This script can is a post processor for CUPS-PDF that adds a visible timestamp to the created document.

It was developed to allow adding documents to a document management system by printing them. The script optionally passes the timestamped PDF to another printer for hardcopy.

## Installation

1. Install *CUPS-PDF*
1. clone repository to `/opt/cups-timestamp`
1. install dependencies, e.g. by creating a `venv` and installing the using `pip`:
    1. `cd /opt/cups-timestamp`
    1. `python -m venv venv`
    1. `source venv/bin/activate`
    1. `pip install -r requirements.txt`
1. copy `cups-pdf-timestamp.conf` to `/etc/cups/`
1. add a new printer to your cups instance, choose `cups-pdf:/timestamp` as connection URI

You can add multiple variants of this script by renaming the *timestamp* part of the conf file and the connection URI. (This is a CUPS-PDF feature.)

## Configuration

You probably want to change some of the variables at the top of `process.py`, e.g the location to put stamped PDFs into or the printer to print them with. You may want to change the locale the locale setting at the top (or comment it to use the user’s locale settings).

The text of the timestamp can be changed by modifying `create_stamp()`, please consider [the documentation for reportlab](https://www.reportlab.com/dev/docs/) if you want to change it.

If you used a different location for the python script you have to change the `PostProcessing` option in `cups-pdf-timestamp.conf`. This file contains plenty of documentation which is worth reading.