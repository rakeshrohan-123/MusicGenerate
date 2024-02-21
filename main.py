from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import logging

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (update this with your specific requirements)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
HEADERS = {"Authorization": "Bearer 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"}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryPayload(BaseModel):
    inputs: str

def query_model(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raise exception for non-2xx response status codes
        return response.content
    except requests.RequestException as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/generate_audio/")
async def generate_audio(payload: QueryPayload):
    if not payload.inputs:
        raise HTTPException(status_code=400, detail="Invalid input data")
    
    audio_bytes = query_model(payload.dict())

    # Encode audio bytes to Base64
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    return {"audio_base64": audio_base64}
