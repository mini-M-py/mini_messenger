import json
from .routers import chat, user, auth
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect, Depends, status, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from . import model, oauth2
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
app.include_router(auth.router)
model.Base.metadata.create_all(bind=engine)

# Custom exception handler for 401 Unauthorized
async def unauthorized_exception_handler(request, exc):
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/Login")

    # Call the default exception handler for other cases
    return await http_exception_handler(request, exc)

# Register the custom exception handler
app.exception_handler(HTTPException)(unauthorized_exception_handler)

#root
@app.get("/")
async def get(request: Request,  user_id: int = Depends(oauth2.get_current_user)):
    extensions = request.query_params.get("extensions", {})
    return templates.TemplateResponse("chat.html", {"request": request, "extensions": extensions})
#login page
@app.get('/Login')
async def get(request: Request):
    extensions = request.query_params.get('extensions', {})
    return templates.TemplateResponse("login.html", {"request":request, "extensions":extensions})

#forget password page
@app.get('/forget_password')
async def get(request: Request):
    extensions = request.query_params.get('extensions', {})
    return templates.TemplateResponse("forget.html", {"request":request, "extensions":extensions})

