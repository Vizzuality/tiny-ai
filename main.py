import json
import os
import uuid
from typing import Dict, Union
import gtts
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from mangum import Mangum
from pydantic import BaseModel

app = FastAPI()

load_dotenv()
secret_token = os.getenv("SECRET_TOKEN")
open_ai_token = os.getenv("OPEN_AI_TOKEN")

mangum_adapter = Mangum(app)

def handler(event, context):
    return mangum_adapter(event, context)
class APIResponse(BaseModel):
    response: str
    audio_url: str
class TokenData(BaseModel):
    token: str
 
class AIRequestBody(BaseModel):
    question: Union[str, Dict]
    context: Union[str, Dict]
    temperature: float = 0.5
    audio: bool = False
    lang: str = 'en'

@app.post("/")
async def index(request: Request, body: AIRequestBody, authorization: str = Header(None)):
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and token == secret_token:
            response = await query_ai(request, body)
            return (response)
    
    raise HTTPException(status_code=401, detail={"error": "Invalid token"})

@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    file_path = os.path.join("temp", filename)

    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}

async def query_ai(request: Request, body: AIRequestBody):
    
    temperature = body.temperature
    context = body.context
    question = body.question
    audio = body.audio
    lang = body.lang
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=temperature, openai_api_key=open_ai_token)

    # Convert the prompt and context to string format, if they are not already
    if isinstance(context, dict):
        context = json.dumps(context)
    if isinstance(question, dict):
        question = json.dumps(question)
    
    idiom = get_language_name(lang)

    question = f"request: {question} Respond in {idiom} idiom"
    
    system_m = f"Please provide concise and specific answers to prompts starting with 'request: '. If you don't know the answer, simply reply with 'I don't know'. Do not mention being an AI or make any references to artificial intelligence. Directly provide the answer if you know it. It's crucial that you only say 'I don't know' in case you cannot answer as I'm asking you."
    
    try:
        response = chat(
            [
                SystemMessage(content=system_m),
                AIMessage(content=question),
                HumanMessage(content=context)
            ]
        )
        if audio == True:
            try: 
                unique_filename = await generate_audio_file(response.content, lang)
                server_url = str(request.base_url)
                audio_url = f"{server_url}audio/{unique_filename}"
            except Exception as e:
                return {"response":response.content, "audio_url": "error 401" }
            return {"response": response.content, "audio_url": audio_url}
        else:
            return {"response": response.content}
    except Exception as e:
        return {"error": str(e)}
    
async def generate_audio_file(text: str, lang: str) -> str:
    tts = gtts.gTTS(text, lang=lang)
    unique_filename = f"{uuid.uuid4().hex}.mp3"
    os.makedirs("temp", exist_ok=True)
    tts.save(os.path.join("temp", unique_filename))
    return unique_filename

def get_language_name(code: str):
    language_codes = {
        'af': 'Afrikaans',
        'ar': 'Arabic',
        'bg': 'Bulgarian',
        'bn': 'Bengali',
        'bs': 'Bosnian',
        'ca': 'Catalan',
        'cs': 'Czech',
        'da': 'Danish',
        'de': 'German',
        'el': 'Greek',
        'en': 'English',
        'es': 'Spanish',
        'et': 'Estonian',
        'fi': 'Finnish',
        'fr': 'French',
        'gu': 'Gujarati',
        'hi': 'Hindi',
        'hr': 'Croatian',
        'hu': 'Hungarian',
        'id': 'Indonesian',
        'is': 'Icelandic',
        'it': 'Italian',
        'iw': 'Hebrew',
        'ja': 'Japanese',
        'jw': 'Javanese',
        'km': 'Khmer',
        'kn': 'Kannada',
        'ko': 'Korean',
        'la': 'Latin',
        'lv': 'Latvian',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'ms': 'Malay',
        'my': 'Myanmar (Burmese)',
        'ne': 'Nepali',
        'nl': 'Dutch',
        'no': 'Norwegian',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ro': 'Romanian',
        'ru': 'Russian',
        'si': 'Sinhala',
        'sk': 'Slovak',
        'sq': 'Albanian',
        'sr': 'Serbian',
        'su': 'Sundanese',
        'sv': 'Swedish',
        'sw': 'Swahili',
        'ta': 'Tamil',
        'te': 'Telugu',
        'th': 'Thai',
        'tl': 'Filipino',
        'tr': 'Turkish',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'vi': 'Vietnamese',
        'zh-CN': 'Chinese (Simplified)',
        'zh-TW': 'Chinese (Mandarin/Taiwan)',
        'zh': 'Chinese (Mandarin)'
    }

    try:
        language = language_codes.get(code)
    except:
        language = "English"
    return language