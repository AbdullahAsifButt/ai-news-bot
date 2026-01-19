from crewai.tools import tool
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


class NewsTools:

    @tool("Search the internet")
    def fetch_news(search_query: str):
        """
        Useful to search the internet for news.
        Input should be a search query string (e.g., 'AI trends 2025').
        Returns the top 2 results strictly limited to 6000 characters to save API tokens.
        """
        url = "https://google.serper.dev/search"

        # We limit to only 2 results to stay under the Rate Limit
        payload = json.dumps(
            {
                "q": search_query,
                "num": 2,
                "tbs": "qdr:w",  # Limits results to the past week ("qdr:w")
            }
        )

        headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json",
        }

        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            results = response.json()

            # Manually clean the data to keep it small
            final_output = ""
            if "organic" in results:
                for item in results["organic"]:
                    final_output += f"Title: {item.get('title')}\n"
                    final_output += f"Link: {item.get('link')}\n"
                    final_output += f"Snippet: {item.get('snippet')}\n"
                    final_output += "----------------\n"

            if not final_output:
                return "No relevant news found."

            # HARD LIMIT: Cut off everything after 2000 characters
            return final_output[:6000]

        except Exception as e:
            return f"Error fetching news: {str(e)}"
