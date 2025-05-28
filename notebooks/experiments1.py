from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
from typing import List, TypedDict

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# === Setup OpenAI model ===
openai_model = ChatOpenAI(model="gpt-4o")

from pydantic import BaseModel

class MeetingDataSchema(BaseModel):
    Meeting_ID: str
    Title: str
    Duration: str
    Attendees: str
    Organizer: str
    Location: str
    MeetingType: str
    MissedbyUser: str
    HasMOM: str
    HasTranscript: str
    MOMContent: str
    TranscriptContent: str
    RecommendedAction: str

# === Tool: Load meeting data ===
@tool
def load_meeting_data() -> List[TypedDict]:
    """Tool to load meeting data from a CSV file."""
    df = pd.read_csv(r"C:\Users\Yaseen Khan\Documents\Data Sceince\Hackathon\Infy_Hackathon\notebooks\yaseen_khan_missed_meetings_2.csv")
    meetings = df.to_dict(orient="records")
    return meetings

# === Tool: Analyze meeting content ===
@tool
def analyze_meeting(meeting: dict) -> str:
    """Analyzes MoM or Transcript from a meeting and returns a summary."""
    mom = meeting.get("MOM Content", "")
    transcript = meeting.get("Transcript Content", "")

    if mom:
        content = f"MoM:\n{mom}"
    elif transcript:
        content = f"Transcript:\n{transcript}"
    else:
        return "No MoM or Transcript available."

    prompt = f"""
    Analyze the following meeting content and summarize key points:

    {content}

    Suggest follow-up actions if any are required for Yaseen Khan.
    """
    response = openai_model.invoke(prompt)
    return response.content

# === Tool: Suggest actions ===
@tool
def suggest_action(summary: str) -> str:
    """Generates action items based on the summary of a meeting."""
    prompt = f"""
    Based on this summary of the meeting:

    {summary}

    Suggest what Yaseen Khan should do next.
    """
    response = openai_model.invoke(prompt)
    return response.content

# === Define LangGraph state ===
class MeetingAgentState(TypedDict):
    current_index: int
    meetings: List[dict]
    actions: List[str]

# === Node function to process each meeting ===
def process_next_meeting(state: MeetingAgentState):
    index = state["current_index"]
    meetings = state["meetings"]
    actions = state.get("actions", [])

    if index >= len(meetings):
        return END

    print(f"Processing Meeting {index + 1}/{len(meetings)}")
    meeting = meetings[index]
    summary = analyze_meeting.invoke(MeetingDataSchema(**meeting))
    action = suggest_action(summary)

    actions.append(f"Meeting {index + 1}: {action}")

    return {
        "current_index": index + 1,
        "meetings": meetings,
        "actions": actions
    }

# === Define LangGraph workflow ===
workflow = StateGraph(MeetingAgentState)
workflow.add_node("process_meeting", process_next_meeting)
workflow.set_entry_point("process_meeting")
workflow.add_conditional_edges(
    "process_meeting",
    lambda state: END if state["current_index"] >= len(state["meetings"]) else "process_meeting",
    {
        "process_meeting": "process_meeting",
        END: END
    }
)

# === Main execution ===
if __name__ == "__main__":
    meetings_data = load_meeting_data.invoke({})

    initial_state = {
        "current_index": 0,
        "meetings": meetings_data,
        "actions": []
    }

    graph = workflow.compile()
    final_state = graph.invoke(initial_state)

    print("\n===== Action Items for Missed Meetings =====")
    for action in final_state["actions"]:
        print(action)
