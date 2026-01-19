from crewai.tools import tool
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
import os
import json


@tool("Log News to Google Sheets")
def log_news(headline: str, summary: str, url: str):
    """
    Useful to log a news item to Google Sheets.
    Input requires specific named arguments: headline, summary, and url.
    """
    # --- VERCEL/GITHUB COMPATIBILITY CHECK ---
    google_creds = os.getenv("GOOGLE_CREDENTIALS_JSON")

    # If running on Cloud (Vercel/GitHub), we need to create the file from the secret
    if os.getenv("VERCEL") or os.getenv("GITHUB_ACTIONS"):
        SERVICE_ACCOUNT_FILE = "credentials.json"
        # Create the file dynamically if it doesn't exist
        with open(SERVICE_ACCOUNT_FILE, "w") as f:
            f.write(google_creds)
    else:
        # Local run
        SERVICE_ACCOUNT_FILE = "AgenticAI\\ai-news-bot\\credentials.json"
    # -----------------------------------------------------------

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    # !!! PASTE YOUR SPREADSHEET ID HERE !!!
    SPREADSHEET_ID = "1dLKfcYQSc-Ydsb7QxcTTbXvFK0T5dfElYPX_76W5FEk"

    try:
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        values = [[today, headline, summary, url]]
        body = {"values": values}

        result = (
            sheet.values()
            .append(
                spreadsheetId=SPREADSHEET_ID,
                range="Sheet1!A:D",
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )

        return f"✅ Logged to Sheets: {headline}"

    except Exception as e:
        return f"❌ Error logging to sheets: {str(e)}"
