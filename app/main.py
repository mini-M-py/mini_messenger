import json
from .routers import chat, user 
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from . import model
from .database import engine
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(user.router)

model.Base.metadata.create_all(bind=engine)


@app.get("/")
async def get(request: Request):
    extensions = request.query_params.get("extensions", {})
    return templates.TemplateResponse("chat.html", {"request": request, "extensions": extensions})

@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)

