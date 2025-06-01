from dotenv import load_dotenv
load_dotenv()
import os
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"]=OPENAI_API_KEY

import pandas as pd
from langgraph.graph import StateGraph,MessagesState, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated, Literal, List
from langchain_core.tools import tool    #for creating Tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver   #To sustain the memory
from langgraph.prebuilt import ToolNode,tools_condition     #To create the Nodes for Tool
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI
openai_model=ChatOpenAI(model="gpt-4o")

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    meetings: list[dict]  # <- This will store the output of load_meeting_data
    analysis: list[str]

@tool
def load_meeting_data() -> List[dict]:
    """Tool to load meeting data from a CSV file."""
    df = pd.read_csv(r"C:\Users\Yaseen Khan\Documents\Data Sceince\Hackathon\Infy_Hackathon\notebooks\yaseen_khan_missed_meetings_2.csv")
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
        response = openai_model.invoke(prompt)
        results.append(f"Meeting {i} Summary:\n{response.content.strip()}")

    return {"analysis": results}

tools=[load_meeting_data]

llm_with_tool=openai_model.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful assistant interact with user gently and upon asked you will load the meeting data and analyze it to provide recommendations.")
def call_model(state:AgentState) -> dict:
    question=state["messages"]  # Get the last message from the state
    response=llm_with_tool.invoke([sys_msg]+question)  #instead of invoking the normal llm , we are using the binding llm which is binded to a tool
    return {"messages":[response]}

tool_node=ToolNode(tools)

def router_function(state: AgentState):    #-> Literal["tools", END]
    message=state["messages"]
    last_message=message[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow=StateGraph(AgentState)

workflow.add_node("assistant",call_model)
workflow.add_node("load_meetings", tool_node)#Consuming tool as node
workflow.add_node("analyze_meetings", analyze_meetings_batch)

workflow.add_edge(START, "assistant")

workflow.add_conditional_edges("assistant",
                               router_function,
                               {"tools": "load_meetings", END:END})
workflow.add_edge("load_meetings", "analyze_meetings")
workflow.add_edge("analyze_meetings", "assistant")
workflow.add_edge("assistant", END)

memory_saver = MemorySaver()
from uuid import uuid4
session_id = str(uuid4())

app = workflow.compile(checkpointer=memory_saver)

# message=[HumanMessage(content="can you load the meeting data and analyse each meeting and recommend the action itmes in each meeting?")]
# response=app.invoke({"messages": message},config={"configurable": {"thread_id": session_id}})
# for m in response["messages"]:
#     m.pretty_print()




# # === CLI LOOP FOR INTERACTIVE CHAT ===
# print("\nWelcome to the Outlook Meeting AI Agent CLI! Type 'exit' to quit.\n")

# while True:
#     user_input = input("> ")
#     if user_input.lower() in ["exit", "quit"]:
#         print("Exiting. Goodbye!")
#         break

#     from langchain_core.messages import HumanMessage
#     message = [HumanMessage(content=user_input)]
#     response = app.invoke({"messages": message}, config={"configurable": {"thread_id": session_id}})

#     for m in response["messages"]:
#         print("\nAI:", m.content)
