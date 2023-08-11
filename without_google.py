import json
import urllib

import httpx
import sqlite_utils


def start_auth_url(client_credentials, scopes):
    url = client_credentials["auth_uri"]
    url += "?" + urllib.parse.urlencode(
        {
            "access_type": "offline",
            "client_id": client_credentials["client_id"],
            "redirect_uri": 'https://localhost:1',
            "response_type": "code",
            "scope": scopes[0]
        }
    )
    return url


scopes = ['https://www.googleapis.com/auth/spreadsheets']

with open("./secrets/credentials.json") as token:
    credentials = json.load(token)
print(credentials)
credentials = credentials["installed"]

# Challenge
# print(f"Get code from URL")
# print(f"URL : {start_auth_url(credentials, scopes)}")
# copied_code = input("copied code")
# response = httpx.post(
#         "https://www.googleapis.com/oauth2/v4/token",
#         data={
#             "code": copied_code,
#             "client_id": credentials["client_id"],
#             "client_secret": credentials["client_secret"],
#             "redirect_uri": "https://localhost:1",
#             "grant_type": "authorization_code",
#         },
#     )
# token = response.json()
#
# with open("./secrets/token.json", "w") as file:
#     json.dump(token, file)
# print(token)

with open("./secrets/token.json", "r") as file:
    ref_token = json.load(file)
print(token)

# refresh token
response = httpx.post(
    "https://www.googleapis.com/oauth2/v4/token",
    data={
        "client_id": credentials["client_id"],
        "client_secret": credentials["client_secret"],
        "refresh_token": ref_token["refresh_token"],
        "grant_type": "refresh_token",
    },
)
refreshed_token = response.json()
print(refreshed_token)

spreadsheet_id = '1mfC6kx1Ex9HBGsd_O9sTxrmYIfxk4tb5DEgIcH3jBT4'
sheet_range = 'Feuille 1'  # TODO : handle default first sheet, params
sheets_request_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{sheet_range}"

response = httpx.get(
    sheets_request_url,
    headers={"Authorization": f"Bearer {refreshed_token['access_token']}"}
)
print(response)
contents = response.json()
print(contents)
values = contents["values"]
keys = values[0]  # first row is keys
# TODO : fill
zipped = [dict(zip(keys, row)) for row in values]
print(zipped)
db = sqlite_utils.Database("example.db", recreate=True)
db["sheet"].insert_all(zipped)

print("Back out")
for row in db["sheet"].rows:
    print(row)
