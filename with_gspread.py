import gspread
import sqlite_utils

FILE_KEY = '1mfC6kx1Ex9HBGsd_O9sTxrmYIfxk4tb5DEgIcH3jBT4'  # example file
gc = gspread.oauth(credentials_filename='secrets/credentials.json', authorized_user_filename='secrets/authorized_user.json')
document = gc.open_by_key(FILE_KEY)
worksheet = document.get_worksheet(0)
db = sqlite_utils.Database("example.db", recreate=True)
print(worksheet.get_all_records())
db["sheet"].insert_all(worksheet.get_all_records())

print(db["sheet"].schema)
for row in db["sheet"].rows:
    print(row)

worksheet = document.get_worksheet(1)
print(worksheet.get_all_records())
db["sheet1"].insert_all(worksheet.get_all_records())

print(db["sheet1"].schema)
for row in db["sheet1"].rows:
    print(row)
