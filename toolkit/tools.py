import os
import pandas as pd
#from langchain.tools import tool
from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults
from typing_extensions import TypedDict, Annotated, Literal, List
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from data_models.model_state import AgentState

model_loader=ModelLoader()
model=model_loader.load_llm
config = load_config()
load_dotenv()

@tool
def load_meeting_data() -> List[dict]:
    """Tool to load meeting data from a CSV file."""
    df = pd.read_csv(r"C:\Users\Yaseen Khan\Documents\Data Sceince\Hackathon\Hack_Project_mini\data\yaseen_khan_missed_meetings_2.csv")
    df = df[0:5]
    meetings = df.to_dict(orient="records")
    return {"meetings": meetings}

def analyze_meetings_batch(state: AgentState) -> list[str]:
    """Analyzes multiple meetings and returns summaries for each."""
    meetings = state.get("meetings", [])
    results = []

    for i, meeting in enumerate(meetings, 1):
        mom = meeting.get("MOM Content", "")
        transcript = meeting.get("Transcript Content", "")

        if mom:
            content = f"MoM:\n{mom}"
        elif transcript:
            content = f"Transcript:\n{transcript}"
        else:
            results.append(f"Meeting {i}: No MoM or Transcript available.")
            continue

        prompt = f"""
        You're an AI assistant of User, responsible for analyzing meeting content which he missed during his leave.
        Your task is to read the content of the meeting, analyze it, and recommend actions such as tasks to complete, follow-up meetings to schedule, or status updates to provide.
        You will be provided with the content of the meeting, and you should summarize it in a concise manner.
        Meeting {i}, conducted on {meeting.get("Date_Time", "")}, 
        which was attended by {meeting.get("Attendees", "")} and then provide recommendations based on your analysis content:
        {content}
        """
        response = model.invoke(prompt)
        results.append(f"Meeting {i} Summary:\n{response.content.strip()}")

    return {"analysis": results}

@tool
def internet_search(state: AgentState) -> (TypedDict):
    """Search the internet for latest information."""
    question=state["messages"]
    response=tavily_tool.invoke(question)
    return {"messages":response}