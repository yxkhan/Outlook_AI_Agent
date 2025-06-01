from fastapi import FastAPI, Request
from pydantic import BaseModel
from outlook_agent import app, session_id  # Import your agent setup
from langchain_core.messages import HumanMessage

# FastAPI instance
fastapi_app = FastAPI()

# Request model
class UserQuery(BaseModel):
    query: str

@fastapi_app.get("/")
def read_root():
    return {"message": "Outlook AI Agent is running!"}

@fastapi_app.post("/chat")
def chat_with_agent(request: UserQuery):
    user_message = request.query
    message = [HumanMessage(content=user_message)]
    
    try:
        response = app.invoke({"messages": message}, config={"configurable": {"thread_id": session_id}})
        ai_reply = "\n".join([m.content for m in response["messages"]])
        return {"response": ai_reply}
    except Exception as e:
        return {"error": str(e)}
