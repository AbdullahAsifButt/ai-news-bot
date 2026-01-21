from crewai import Crew, Task
from agents import get_news_researcher, get_news_writer

researcher = get_news_researcher()
writer = get_news_writer()

search_task = Task(
    description="""
    Search for the top 5 latest and most significant news trends regarding: {topic}.
    Focus on events from the last 7 days. 
    Identify key companies, new technologies, or major market shifts.
    """,
    expected_output="A list of raw news findings with titles, links, and brief details.",
    agent=researcher,
)

summarize_task = Task(
    description="""
    1. Summarize the news into a markdown-formatted daily briefing (headline, summary, url).
    2. **MANDATORY**: Use the 'Send News to Slack' tool to send that summary.
    3. **MANDATORY**: Iterate through every news item and use the 'Log News to Google Sheets' tool for each one.
    
    IMPORTANT: Do NOT return the news summary as your Final Answer. 
    Your Final Answer should ONLY be the text: "Briefing sent to Slack and logged to Sheets."
    """,
    expected_output="A simple confirmation message confirming the tools were successfully used.",
    agent=writer,
)

news_crew = Crew(
    agents=[researcher, writer], tasks=[search_task, summarize_task], verbose=True
)

topic = "Artificial Intelligence trends 2025"
print(f"🚀 Starting the News Crew on topic: {topic}...")

result = news_crew.kickoff(inputs={"topic": topic})
print(result)
