import uvicorn
import multiprocessing

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def main():
    print(f"Child process PID : {multiprocessing.current_process().pid}")
    uvicorn.run("main:app", host="0.0.0.0", port=80, workers=4, log_level="info")
