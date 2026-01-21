from crewai import Agent, LLM
from tools_news import NewsTools
from tools_slack import SlackTools
from tools_sheets import SheetsTools
import os
from dotenv import load_dotenv

load_dotenv()


llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


def get_news_researcher():
    """
    Agent 1: The Researcher.
    Role: Finds the news.
    Tools: Can use Google Search (Serper).
    """
    return Agent(
        role="Senior Tech News Researcher",
        goal="Uncover the latest breaking news and trends in {topic}",
        backstory="""You are a seasoned journalist with a nose for big stories. 
        You are expert at using search tools to find the most relevant 
        and recent information on the internet. You ignore clickbait 
        and focus on factual, high-impact changes.""",
        tools=[NewsTools.fetch_news],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def get_news_writer():
    """
    Agent 2: The Writer.
    Role: Summarizes the news.
    Tools: Slack and Google Sheets.
    """
    return Agent(
        role="Tech News Summarizer",
        goal="Summarize findings, post them to Slack, and save them to Google Sheets.",
        backstory="""You are an expert editor and publisher. 
        You take raw news data and turn it into professional updates.
        You are responsible for broadcasting this news to the team via Slack
        and archiving it in the database (Google Sheets).""",
        tools=[SlackTools.send_news_to_slack, SheetsTools.log_news],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
