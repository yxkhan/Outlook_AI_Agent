import pandas as pd
from langgraph.graph import StateGraph,MessagesState, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated, Literal, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver   #To sustain the memory
from langgraph.prebuilt import ToolNode,tools_condition     #To create the Nodes for Tool
from utils.model_loader import ModelLoader
from toolkit.tools import *
from data_models.model_state import AgentState

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    meetings: list[dict]  # <- This will store the output of load_meeting_data
    analysis: list[str]

class GraphBuilder:
    def __init__(self):
        self.model_loader=ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.tools = [load_meeting_data, internet_search]
        self.analyze_meetings = analyze_meetings_batch
        llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.llm_with_tools = llm_with_tools
        self.memory_saver = MemorySaver()
        self.graph = None
    
    def _chatbot_node(self,state:AgentState) -> dict:
         return {"messages": [self.llm_with_tools.invoke(state["messages"])]}
    
    def _router_function(self,state: AgentState):
        last_message=state["messages"][-1]
        if last_message.tool_calls:
            return "tools"
        return END

    def build(self):
        graph_builder = StateGraph(AgentState)
        
        graph_builder.add_node("assistant", self._chatbot_node)
        
        tool_node=ToolNode(tools=self.tools)
        graph_builder.add_node("load_meetings", tool_node)
        graph_builder.add_node("analyze_meetings", self.analyze_meetings)

        graph_builder.add_edge(START, "assistant")        
        graph_builder.add_conditional_edges("assistant",
                                            self._router_function,
                                            {"tools": "load_meetings", END:END})
        graph_builder.add_edge("load_meetings", "analyze_meetings")
        graph_builder.add_edge("analyze_meetings", "assistant")
        graph_builder.add_edge("assistant", END)

        memory_saver=self.memory_saver
        self.graph = graph_builder.compile(checkpointer=memory_saver)
        return self.graph
        
    def get_graph(self):
        if self.graph is None:
            raise ValueError("Graph not built. Call build() first.")
        return self.graph
