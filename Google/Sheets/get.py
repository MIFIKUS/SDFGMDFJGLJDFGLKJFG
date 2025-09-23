from Google.Sheets.auth import SPREADSHEET_URL, get_gspread_service, SHEET_NAME
from config import CONFIG

service = get_gspread_service()
cell_num = CONFIG['cell_num']


def get_max_tables() -> int:
    try:
        cell = f'D{cell_num}'

        spreadsheet = service.open_by_url(SPREADSHEET_URL)
        worksheet = spreadsheet.worksheet(SHEET_NAME)

        return int(worksheet.acell(cell).value)
    except:
        return 0 

