import io
import uvicorn
import subprocess
import os
import re
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
import whisper
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware




class VideoRequest(BaseModel):
    url : str
    # format : str #.mp3 or .mp4

load_dotenv()
app = FastAPI()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/") #get - read data
async def health() -> dict:
    """
    Root API endpoint to check the health of the service.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Hello World"}



@app.post("/submit") #post - create data
async def submit(video_link: VideoRequest):
    """
    Endpoint to convert video links to recipes to storage
    """

    url = video_link.url

    
    # Step 1: Request Cobalt API to convert video to MP3
    try:
        # Define the Cobalt API URL
        cobalt_api = "http://localhost:9000/"

        # Define the request headers
        headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
        }

        # Define the request body
        body = {
        "url": url,
        "audioFormat": "mp3",
        "downloadMode": "audio",
        "tiktokFullAudio": True
        }

        # Send the POST request
        response = requests.post(cobalt_api, json=body, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Cobalt conversion failed")

        response_data = response.json()
        mp3_url = response_data.get("url")  # URL of the generated MP3

        if not mp3_url:
            raise HTTPException(status_code=500, detail="MP3 URL not found in response")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Cobalt: {str(e)}")
    
    step = 1
    
    #####################################
    
    # Step 2: Download the MP3 file
    try:
        mp3_response = requests.get(mp3_url)

        if mp3_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to download MP3")

        audio_stream = io.BytesIO(mp3_response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading MP3: {str(e)}")
    
    step = 2
    try:
        audio_stream.seek(0)  # Reset the stream position
        audio_content = audio_stream.read()

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                """Provide the transcription for this cooking recipe audio clip

                use this json schema:
                {
                    prep_time : int
                    cooking_time : int
                    total_time : int
                    ingredients : [{item: str, qty: int, unit: str}]
                    instructions : [str]
                }
                """,
                types.Part.from_bytes(
                    data=audio_content,
                    mime_type='audio/mp3'
                )
            ]
        )
        
        transcript = response.text

    except Exception as e:
        # Print the full exception for debugging
        import traceback
        print(f"Full exception: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error in transcription: {str(e)}")
    
    step = 3
    

    # **Step 1: Remove triple backticks**
    cleaned_transcript = re.sub(r"```json|```", "", transcript).strip()

    cleaned_object = json.loads(cleaned_transcript)

    # For debugging purposes, let's print the transcript
    print(f"Transcript: {type(cleaned_object)}")

    # cleaned_transcript = jsonable_encoder(cleaned_transcript)

    return JSONResponse(content=cleaned_object)
