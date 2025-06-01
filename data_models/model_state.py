from typing_extensions import TypedDict, Annotated, Literal, List
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    meetings: list[dict]  # <- This will store the output of load_meeting_data
    analysis: list[str]