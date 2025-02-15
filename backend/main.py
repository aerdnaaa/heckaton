import io
import uvicorn
from google import genai
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

class VideoRequest(BaseModel):
    video : str
    # format : str #.mp3 or .mp4

load_dotenv()
app = FastAPI()
client = genai.Client()
load_dotenv()
os.getenv("GOOGLE_API_KEY")

@app.get("/")
async def health() -> dict:
    """
    Root API endpoint to check the health of the service.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Hello World"}



@app.post("/submit")
async def submit(video_link: VideoRequest) -> JSONResponse:
    """
    Endpoint to convert video links to recipes to storage
    """

    url = video_link.url



    # cobalt_response = 
    myfile = client.files.upload(file=cobalt_response.url)

    response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        'Provide the transcription for this audio clip',
        myfile,
    ]
)
    ## put transcript into llm to organise into recipe
    ## format recipe into json

    content={"trasncript" : response.text} ## temp commented out
        # "prep_time" : 
        # cooking_time : response.prep_time
        # total_time : int
        # ingredients : (item, qty, unit) [(str,int,str)]
        # instructions : [str]
        # }
    return JSONResponse(content=content)
