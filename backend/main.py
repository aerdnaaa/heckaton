import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

class VideoRequest(BaseModel):
    url : str
    # format : str #.mp3 or .mp4

app = FastAPI()


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

    ## put url into cobalt
    ## obtain mp3 from cobalt
    ## put mp3 into openai whisper/gemini, get transcript
    ## put transcript into llm to organise into recipe
    ## format recipe into json

    content={"video_link" : url} ## temp commented out
        # "prep_time" : 
        # cooking_time : response.prep_time
        # total_time : int
        # ingredients : (item, qty, unit) [(str,int,str)]
        # instructions : [str]
        # }
    return JSONResponse(content=content)
