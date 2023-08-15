import json
import pathlib
import urllib

import click
import httpx


def start_auth_url(client_id, scope):
    AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
    url = AUTH_URI
    url += "?" + urllib.parse.urlencode(
        {
            "access_type": "offline",
            "client_id": client_id,
            "redirect_uri": 'https://localhost:1',
            "response_type": "code",
            "scope": scope
        }
    )
    return url


def _auth_copied_code_request(copied_code, client_id, client_secret):
    response = httpx.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data={
            "code": copied_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "https://localhost:1",
            "grant_type": "authorization_code",
        },
    )
    response.json()
    return response.json()


def _save_auth_token(filepath, token):
    with open(filepath, "w") as fp:
        fp.write(json.dumps(token, indent=4))
    pathlib.Path(filepath).chmod(0o600)


def _refresh_token_request(client_id, client_secret, refresh_token):
    response = httpx.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )
    return response.json()["access_token"]


def _auth_challenge(client_id, client_secret):
    SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    print(f"Please copy & paste the following URL into a web browser and authorize the request.")
    print(f"Then copy & paste the code you obtain in the URL (your browser should give you an error) below:\n")
    copied_code = input("Code: ")
    response = _auth_copied_code_request(copied_code, client_id, client_secret)
    refresh_token = response["refresh_token"]
    return {'client_id': client_id, 'client_secret': client_secret, 'refresh_token': refresh_token}


def load_tokens(auth):
    token_info = json.load(open(auth))
    return {
        "access_token": token_info["access_token"],
        "refresh_token": token_info["refresh_token"],
        "client_id": token_info["client_id"],
        "client_secret": token_info["client_secret"]
    }


def _get_sheets(access_token, spreadsheet_id):
    sheets_request_url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?fields=sheets.properties.title'
    response = httpx.get(
        sheets_request_url,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code == httpx.codes.OK:
        contents = response.json()
        return [sheet['properties']['title'] for sheet in contents['sheets']]
    else:
        print(response)
        click.ClickException("Error when getting data...")


def _get_data(access_token, spreadsheet_id, sheet_range):
    sheets_request_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_range}"
    response = httpx.get(
        sheets_request_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    if response.status_code == httpx.codes.OK:
        return response.json()
    else:
        print(response.json().message)
        click.ClickException("Error when getting data...")
