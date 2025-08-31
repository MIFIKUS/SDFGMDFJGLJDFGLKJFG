import gspread
from google.oauth2.service_account import Credentials


SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/18SOvJ1o8NiasANGlPMyIz7MmYki7zpQk1GWZ_DBYW-o'
SHEET_NAME = 'WPN'
PATH_TO_CREDS = 'Google\\credentials.json'

def get_gspread_service():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"

    ]
    credentials = Credentials.from_service_account_file(
        PATH_TO_CREDS, 
        scopes=scopes
    )
    return gspread.authorize(credentials)

