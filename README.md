# Google-Sheets-to-SQLite tool

Create a SQLite database containing data from a [Google Sheets](https://www.google.com/sheets) document.

Google Sheets provides a simple way to collect and work on data in a collaborative way. However, publishing data can be hassle. 

This tool can download spreadsheet data and store them in an SQLite database.

This lets you use SQL to analyze your data, using [Datasette](https://datasette.io/) or the SQLite command-line tool or any other SQLite database browsing software.

## Installation

Install this tool using `pip` in the repository root:

    pip install .

## Quickstart

Get you Google Developer account ready:

1. Create a Google Developer Project: https://console.cloud.google.com/projectcreate
2. OAuth Consent Screen: [click here](https://console.cloud.google.com/apis/credentials/consent) then choose External and add an app, add `https://www.googleapis.com/auth/spreadsheets.readonly` to the scopes and an account you have access to as a Test user. The Test user should have access to the documents you want to import with this tool.
3. Create OAuth 2.0 Credentials: [click here](https://console.cloud.google.com/apis/credentials). These credentials are needed below. 
4. Activate the Sheets API : [click here](https://console.developers.google.com/apis/api/sheets.googleapis.com/overview) and "Enable" the Google Sheets API without which your requests will be rejected with a code 403.

Authenticate with Google Sheets with the credentials you created above:

    google-sheets-to-sqlite authenticate --id <client id> <client secret>

Now create a SQLite database with the data in "Sheet 1" of document with sheet id "sheet_id":

    google-sheets-to-sqlite get database.db table_name sheet_id "Sheet 1"

You can explore the resulting database using [Datasette](https://datasette.io/):

    $ pip install datasette
    $ datasette database.db
    INFO:     Started server process [24661]
    INFO:     Uvicorn running on http://127.0.0.1:8001


## TODO

- Tests
- pypi package, CI?
- Handle primary key from data
- Handle partial arguments (missing table, missing sheet name, ...)
- Handle datatypes?
- Handle multiple sheets