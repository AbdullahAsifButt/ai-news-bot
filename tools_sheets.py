from crewai.tools import tool
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
import os


class SheetsTools:

    @tool("Log News to Google Sheets")
    @tool("Log News to Google Sheets")
    def log_news(headline: str, summary: str, url: str):
        """
        Useful to log a news item to Google Sheets.
        Input requires specific named arguments: headline, summary, and url.
        """
        # --- VERCEL FIX: Create credentials in /tmp from Env Var ---
        import os
        import json

        # We will store the JSON content in an Environment Variable
        google_creds = os.getenv("GOOGLE_CREDENTIALS_JSON")

        # Determine path based on environment (Vercel uses /tmp, Local uses current dir)
        if os.getenv("VERCEL"):
            SERVICE_ACCOUNT_FILE = "/tmp/credentials.json"
        else:
            SERVICE_ACCOUNT_FILE = "credentials.json"

        # Create the file dynamically
        with open(SERVICE_ACCOUNT_FILE, "w") as f:
            f.write(google_creds)
        # -----------------------------------------------------------

        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        # UPDATE THIS WITH YOUR ACTUAL ID
        SPREADSHEET_ID = "1dLKfcYQSc-Ydsb7QxcTTbXvFK0T5dfElYPX_76W5FEk"

        try:
            creds = Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()

            # Prepare the Data
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            values = [[today, headline, summary, url]]
            body = {"values": values}

            # Append to Sheet
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


# --- TEST CODE ---
if __name__ == "__main__":
    print("📊 Testing Google Sheets Tool...")

    # Run the function directly
    result = SheetsTools.log_news.run(
        headline="AI Takes Over World",
        summary="Just kidding, it's just a test.",
        url="http://google.com",
    )
    print(result)
