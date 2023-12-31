import click
import sqlite_utils

from .utils import load_tokens, _auth_challenge, _refresh_token_request, _save_auth_token, _get_data

# default values
DEFAULT_SPREADSHEET_ID = '1Zx7Aieu8XmXLKe5kkce9IUfWpRtiwC7InvVR6HImJHI'
DEFAULT_SHEET_RANGE = 'Sheet1'  # TODO : handle default first sheet, params


# constants
# SCOPE = 'https://www.googleapis.com/auth/spreadsheets'


# Authentication flow : from client id and secret, get refresh_token and keep the three in a json file.
# In documentation and "quickstart" highlight that this code allows you to *create* an app but not to connect to Google
# directly.


@click.group()
def cli():
    """Create a SQLite database with data stored in a Google Sheets document."""
    pass


@cli.command()
@click.option(
    "--id",
    type=str,
)
@click.option(
    "--secret",
    type=str,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file.",
)
def authenticate(id, secret, auth):
    token_exists = True
    try:
        token = load_tokens(auth)
    except (KeyError, FileNotFoundError):
        token_exists = False
        if not id or not secret:
            raise click.ClickException(
                "Credentials not found. Please create credentials file or use --id and --secret options.")

    if not token_exists:
        try:
            token = _auth_challenge(id, secret)
        except:
            raise click.ClickException("Error getting token from credentials")

    token["access_token"] = _refresh_token_request(token["client_id"], token["client_secret"], token["refresh_token"])

    _save_auth_token(auth, token)
    click.echo("ok")


@cli.command()
@click.argument(
    "database",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
)
@click.argument(
    "table",
    type=str,
    required=False
)
@click.argument("spreadsheet_id")
@click.argument("sheet_range")
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file.",
)
@click.option(
    "-h",
    "--header",
    default=0,
    help="Header row index. If all sheets are imported, header row index is common."
)
def get(database, table, spreadsheet_id, sheet_range, auth, header):
    access_token = None
    try:
        auth_tokens = load_tokens(auth)
        access_token = auth_tokens["access_token"]
    except FileNotFoundError:
        click.ClickException("Auth token not found. Wrong path or use authenticate first.")

    db = sqlite_utils.Database(database, recreate=True)
    contents = _get_data(access_token, spreadsheet_id, sheet_range)
    # TODO: understand need to refresh
    values = contents["values"]
    keys = values[header]  # first row is keys
    zipped = [dict(zip(keys, row)) for row in values[header + 1:]]
    db[table].insert_all(zipped)