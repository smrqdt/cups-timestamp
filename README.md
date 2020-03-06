This script is a post processor for CUPS-PDF that adds a visible timestamp to the created document.

It was developed to allow adding documents to a document management system by printing them, while also receiving a hardcooy with an date of receipt stamp..

## Installation

1. Install *CUPS-PDF*
1. clone repository to `/opt/cups-timestamp`
1. install dependencies, e.g. by creating a `venv` and installing the using `pip`:
    1. `cd /opt/cups-timestamp`
    1. `python3 -m venv venv`
    1. `venv/bin/pip install -r requirements.txt`
1. copy `/etc/cups/cups-pdf.conf` to `/etc/cups/cups-pdf-timestamp.conf` (or any other name that matches `cups-pdf-*.conf`)
1. add the location of `process.py` as value of `PostProcessing` in the conf file
1. add a new printer to your cups instance, choose `cups-pdf:/timestamp` as connection URI (the web interface should offer you to configure *CUPS-PDF (Virtual timestamp Printer)*)
    * as driver select *Generic* → *Generic CUPS-PDF Printer (no options)*

You can add multiple variants of this script by renaming the *timestamp* part of the conf filegit name and in the connection URI. (This is a CUPS-PDF feature.)

## Configuration

You probably want to change some of the variables at the top of `process.py`, e.g the location to put stamped PDFs into or the printer to print them with. You may want to change the locale setting at the top (or comment it to use the user’s locale settings).

The text of the timestamp can be changed by modifying `create_stamp()`, please consider [the documentation for reportlab](https://www.reportlab.com/dev/docs/) if you want to change it.

