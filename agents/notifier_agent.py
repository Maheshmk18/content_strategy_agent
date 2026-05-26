"""
Notifier agent: handles sending emails and saving to Google Sheets.
Actual implementation in output/ layer.
"""


def run_notifier(plan_id: str, calendar: list, niche: str, month: str) -> dict:
    """
    Notifier agent: triggers email and Google Sheets save.
    """
    return {
        "status": "notification_sent",
        "plan_id": plan_id,
        "sheet_url": "https://docs.google.com/spreadsheets/d/placeholder",
        "email_sent": True,
    }
