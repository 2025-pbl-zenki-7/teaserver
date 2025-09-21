from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .config import get_tea_config, save_tea_config
from .llm import get_emotion_and_response, update_chat_prompt
from .arduino import send_tea_command
import json
import os

app = FastAPI()

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Path to the frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

# Mount the frontend directory as static files
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")


class TeaConfig(BaseModel):
    teas: dict[str, str]


@app.get("/")
def read_root():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))


@app.get("/config")
def read_config_page():
    return FileResponse(os.path.join(frontend_dir, 'config.html'))


@app.get("/api/config")
def read_config():
    return {"teas": get_tea_config()}


@app.post("/api/config")
def update_config(config: TeaConfig):
    save_tea_config(config.model_dump())
    update_chat_prompt()
    return {"status": "success"}


@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        ai_response = get_emotion_and_response(data)

        # Serve tea and finish chat when tea_type is specified
        if ai_response.tea_type:
            send_tea_command(f"{ai_response.tea_type},{
                             ai_response.sugar_amount},{ai_response.milk_amount}")
            response_with_tea = f"{ai_response.response} お茶をどうぞ。"
            update_chat_prompt()
        else:
            response_with_tea = ai_response.response

        await websocket.send_text(json.dumps({
            "emotion": ai_response.emotion,
            "response": response_with_tea,
            "tea": ai_response.tea_type,
            "sugar": ai_response.sugar_amount,
            "milk": ai_response.milk_amount
        }))
