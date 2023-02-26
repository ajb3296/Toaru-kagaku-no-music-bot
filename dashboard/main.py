import uvicorn
import multiprocessing

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from musicbot.utils.statistics import Statistics


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/statistics/week")
async def get_week(request: Request):
    return templates.TemplateResponse("week.html", {"request": request})

def main():
    """ multiprocessing 으로 실행해야함 """
    print(f"Child process PID : {multiprocessing.current_process().pid}")
    # 공유기 포트포워딩 설정에서 내부 8000번 포트를 외부 80번 포트로 포워딩
    # 80번 포트로 열면 권한 문제가 발생할 수 있음
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4, log_level="info")
