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

# ... (Agents initialization remains the same) ...

# Task 1: Search (Kept the same)
search_task = Task(
    description="""
    Search for the top 5 latest and most significant news trends regarding: {topic}.
    Focus on events from the last 7 days. 
    Identify key companies, new technologies, or major market shifts.
    """,
    expected_output="A list of raw news findings with titles, links, and brief details.",
    agent=researcher,
)

# Task 2: Summarize & Publish (UPDATED)
summarize_task = Task(
    description="""
    You have received a list of news from the Researcher. 
    
    STEP 1: Summarize
    Create a clean daily briefing with bullet points. Each point must have a Headline, Summary, and Link.
    
    STEP 2: Publish to Slack
    Use the 'Send News to Slack' tool to post the *entire* summary as one message.
    
    STEP 3: Archive to Sheets
    For EACH news item in the list, use the 'Log News to Google Sheets' tool. 
    You must call this tool multiple times (once for every news item) to log them individually.
    """,
    expected_output="A confirmation that the news was posted to Slack and logged to Sheets.",
    agent=writer,
)

# ... (Rest of the file remains the same) ...

news_crew = Crew(
    agents=[researcher, writer], tasks=[search_task, summarize_task], verbose=True
)


def run_news_crew():
    topic = "Artificial Intelligence trends 2025"
    print(f"🚀 Starting the News Crew on topic: {topic}...")
    result = news_crew.kickoff(inputs={"topic": topic})
    return result


# Only run immediately if we are testing locally
if __name__ == "__main__":
    run_news_crew()
# Trigger Vercel Build
