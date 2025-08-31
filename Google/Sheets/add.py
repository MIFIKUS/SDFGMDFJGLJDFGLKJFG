from Google.Sheets.auth import SPREADSHEET_URL, get_gspread_service, SHEET_NAME
from config import CONFIG

service = get_gspread_service()
cell_num = CONFIG['cell_num']


def set_status(status: str):
    cell = f'B{cell_num}'

    spreadsheet = service.open_by_url(SPREADSHEET_URL)
    worksheet = spreadsheet.worksheet(SHEET_NAME)

    worksheet.update(cell, status)


def set_amount_of_opened_tables(opened_tables: int):
    cell = f'C{cell_num}'

    spreadsheet = service.open_by_url(SPREADSHEET_URL)
    worksheet = spreadsheet.worksheet(SHEET_NAME)

    worksheet.update(cell, str(opened_tables))





