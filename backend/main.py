from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/submit")
async def root():
    return {"message": "testinttsitneint"}
