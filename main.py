# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# #from outlook_agent import app as agent_app, session_id
# from langchain_core.messages import HumanMessage
# import webbrowser
# import threading
# from Agent.agentic_wrkflw import GraphBuilder
# from uuid import uuid4


# session_id = str(uuid4())
# graph_builder = GraphBuilder()
# agent_app = graph_builder.build()  # <- build returns the compiled graph

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# # Launch browser automatically
# def open_browser():
#     webbrowser.open("http://127.0.0.1:8000")

# threading.Timer(1.5, open_browser).start()

# @app.get("/", response_class=HTMLResponse)
# async def serve_chat_ui(request: Request):
#     return templates.TemplateResponse("chat.html", {"request": request})

# @app.post("/chat")
# async def chat(request: Request):
#     data = await request.json()
#     user_input = data["message"]
#     response = agent_app.invoke({"messages": [HumanMessage(content=user_input)]},
#                                 config={"configurable": {"thread_id": session_id}})
#     return {"response": response["messages"][-1].content}

# from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from langchain_core.messages import HumanMessage
import webbrowser
import threading
from Agent.agentic_wrkflw import GraphBuilder
from uuid import uuid4

session_id = str(uuid4())

graph_builder = GraphBuilder()
agent_app = graph_builder.build()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

threading.Timer(1.5, open_browser).start()

@app.get("/", response_class=HTMLResponse)
async def serve_chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data["message"]
    response = agent_app.invoke({"messages": [HumanMessage(content=user_input)]},
                                config={"configurable": {"thread_id": session_id}})
    return {"response": response["messages"][-1].content}

app.mount("/static", StaticFiles(directory="static"), name="static")
