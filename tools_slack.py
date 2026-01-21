from crewai.tools import tool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

load_dotenv()


class SlackTools:

    @tool("Send News to Slack")
    def send_news_to_slack(news_summary: str):
        """
        Useful to send the summarized news report to a specific Slack channel.
        The input should be the full markdown string of the news summary.
        """
        token = os.getenv("SLACK_BOT_TOKEN")
        channel = os.getenv("SLACK_CHANNEL_ID")

        if not token:
            return "Error: SLACK_BOT_TOKEN not found in .env"

        client = WebClient(token=token)

        try:
            response = client.chat_postMessage(
                channel=channel,
                text=news_summary,
                unfurl_links=False,
            )
            return f"Successfully sent news to channel {channel}"

        except SlackApiError as e:
            return f"Error sending to Slack: {e.response['error']}"
