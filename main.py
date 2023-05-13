from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Union
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json
from mangum import Mangum

app = FastAPI()

load_dotenv()
secret_token = os.getenv("SECRET_TOKEN")
open_ai_token = os.getenv("OPEN_AI_TOKEN")

mangum_adapter = Mangum(app)

def handler(event, context):
    return mangum_adapter(event, context)

class TokenData(BaseModel):
    token: str

class AIRequestBody(BaseModel):
    question: Union[str, Dict]
    context: Union[str, Dict]
    temperature: float = 0.5

@app.post("/")
async def index(body: AIRequestBody, authorization: str = Header(None)):
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and token == secret_token:
            response = query_ai(body)
            return (response)
    
    raise HTTPException(status_code=401, detail={"error": "Invalid token"})

def query_ai(body: AIRequestBody):
    
    temperature = body.temperature
    context = body.context
    question = body.question
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature, openai_api_key=open_ai_token)

    # Convert the prompt and context to string format, if they are not already
    if isinstance(context, dict):
        context = json.dumps(context)
    if isinstance(question, dict):
        question = json.dumps(question)

    question = f"request: {question}"
    
    system_m = "Please provide concise and specific answers to prompts starting with 'request: '. If you don't know the answer, simply reply with 'I don't know'. Do not mention being an AI or make any references to artificial intelligence. Directly provide the answer if you know it. It's crucial that you only say 'I don't know' in case you cannot answer how I said before."
    
    try:
        response = chat(
            [
                SystemMessage(content=system_m),
                AIMessage(content=question),
                HumanMessage(content=context)
            ]
        )

        return {"response": response.content}
    
    except Exception as e:
        return {"error": str(e)}
    