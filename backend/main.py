import io
import uvicorn
import subprocess
import os 
import whisper
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


class VideoRequest(BaseModel):
    url : str
    # format : str #.mp3 or .mp4

app = FastAPI()

model = whisper.load_model("small")

@app.get("/") #get - read data
async def health() -> dict:
    """
    Root API endpoint to check the health of the service.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Hello World"}



@app.post("/submit") #post - create data
async def submit(video_link: VideoRequest) -> JSONResponse:
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
        data = {
        "url": "https://www.youtube.com/watch?v=O78NzcXf2sw",
        "audioFormat": "mp3",
        "downloadMode": "audio",
        "tiktokFullAudio": True
        }

        # Send the POST request
        response = requests.post(cobalt_api, json=data, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Cobalt conversion failed")

        response_data = response.json()
        print(response_data)
        mp3_url = response_data.get("url")  # URL of the generated MP3

        if not mp3_url:
            raise HTTPException(status_code=500, detail="MP3 URL not found in response")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Cobalt: {str(e)}")
    
    # Step 2: Download the MP3 file
    try:
        mp3_response = requests.get(mp3_url)

        if mp3_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to download MP3")

        audio_stream = io.BytesIO(mp3_response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading MP3: {str(e)}")

    
    # # Step 2: Load the audio into Whisper from memory (as a file-like object)
    #     audio_stream = io.BytesIO(process.stdout)
    #     transcript = model.transcribe(audio_stream)

    #     return {"message": "Transcription successful", "transcript": transcript["text"]}

    # except subprocess.CalledProcessError as e:
    #     raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    ## put url into cobalt
    ## obtain mp3 from cobalt
    ## put mp3 into openai whisper/gemini, get transcript
    ## put transcript into llm to organise into recipe
    ## format recipe into json

    # content={response_data} ## temp commented out
        # "prep_time" : 
        # cooking_time : response.prep_time
        # total_time : int
        # ingredients : (item, qty, unit) [(str,int,str)]
        # instructions : [str]
        # }
    return JSONResponse(content=response_data)
