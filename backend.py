from dotenv import load_dotenv
load_dotenv()
from typing import List

## Setup Pydantic Model for schema Validation
from pydantic import BaseModel

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    prompt: str
    messages: List[str]
    allow_search: bool
    
## Setup AI Agent from Frontend Request
from fastapi import FastAPI
from agent import get_response_from_agent

ALLOWED_MODEL_NAMES=["gpt-4o-mini","llama-3.3-70b-versatile"]

app=FastAPI(title="LangGraph AI Agent")

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model."}
    
    llm_id=request.model_name
    query=request.messages
    allow_search=request.allow_search
    prompt=request.prompt
    provider=request.model_provider
    
    # Create AI agent
    response=get_response_from_agent(llm_id, query, allow_search, prompt, provider)
    return response

## Run app and explore Swagger UI Docs
if __name__ =="__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)
