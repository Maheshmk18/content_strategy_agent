from config.settings import settings
from graph.state import DayEntry
from langsmith import traceable
import gspread
from google.oauth2.service_account import Credentials
import json


@traceable(name="create_calendar_sheet")
async def create_calendar_sheet(calendar: list[DayEntry], month: str) -> str:
    """Create a Google Sheet with the content calendar and return the URL."""
    try:
        # Get service account credentials
        creds_dict = settings.get_google_service_account()
        if not creds_dict:
            return "https://docs.google.com/spreadsheets/d/error-no-credentials"

        # Authenticate with Google Sheets API
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)

        # Create new spreadsheet
        sheet_title = f"Content Calendar - {month}"
        spreadsheet = client.create(sheet_title)
        worksheet = spreadsheet.sheet1

        # Format and write calendar data
        rows = format_calendar_for_sheet(calendar)
        worksheet.append_rows(rows)

        # Format header row
        worksheet.format("1:1", {
            "backgroundColor": {"red": 0.2, "green": 0.6, "blue": 0.9},
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}
        })

        # Make sheet publicly readable (instead of sharing with specific user)
        try:
            spreadsheet.share("", perm_type='anyone', role='reader')
        except Exception as share_error:
            print(f"Note: Sheet created but public access could not be set: {share_error}")

        # Return the spreadsheet URL
        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}"
        return sheet_url

    except Exception as e:
        error_msg = str(e)
        print(f"Error creating Google Sheet: {error_msg}")
        import traceback
        traceback.print_exc()
        return f"https://docs.google.com/spreadsheets/d/error-{error_msg[:50]}"


@traceable(name="format_calendar_for_sheet")
def format_calendar_for_sheet(calendar: list[DayEntry]) -> list[list]:
    """Format calendar into rows for Google Sheets."""
    rows = [["Day", "Date", "Platform", "Content Type", "Topic", "Notes"]]

    for day_entry in calendar:
        row = [
            day_entry["day"],
            day_entry["date"],
            day_entry["platform"],
            day_entry["content_type"],
            day_entry["topic"],
            day_entry["notes"],
        ]
        rows.append(row)

    return rows
