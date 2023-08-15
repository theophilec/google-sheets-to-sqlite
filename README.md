# Google-Sheets-to-SQLite tool

Create a SQLite database containing data from a [Google Sheets](https://www.google.com/sheets) document.

Google Sheets provides a simple way to collect and work on data in a collaborative way. However, publishing data can be hassle. 

This tool can download spreadsheet data and store them in an SQLite database.

This lets you use SQL to analyze your data, using [Datasette](https://datasette.io/) or the SQLite command-line tool or any other SQLite database browsing software.

## Installation

Install this tool using `pip` in the repository root:

    pip install .

## Quickstart

Authenticate with Google Sheets by running:

    google-sheets-to-sqlite authenticate

Now create a SQLite database with the data in "Sheet 1" of document with sheet id "sheet_id":

    google-sheets-to-sqlite get database.db table_name sheet_id "Sheet 1"

You can explore the resulting database using [Datasette](https://datasette.io/):

    $ pip install datasette
    $ datasette database.db
    INFO:     Started server process [24661]
    INFO:     Uvicorn running on http://127.0.0.1:8001


## TODO

- Tests
- pip package, CI?
- Handle primary key from data
- Handle partial arguments (missing table, missing sheet name, ...)
- Handle datatypes?
- Handle multiple sheets