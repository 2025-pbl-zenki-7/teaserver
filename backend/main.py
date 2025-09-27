from .llm import AIResponse
import os
from .arduino import send_tea_command
from .llm import get_emotion_and_response, update_chat_prompt
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket
from starlette.responses import FileResponse
from contextlib import asynccontextmanager
from . import gpio


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


@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


class FrontendResponse(BaseModel):
    emotion: str
    response: str
    tea: int | None
    sugar: int
    milk: int
    finished: bool


@app.websocket("/api/chat")
async def chat(websocket: WebSocket):
    # Add the new client to the connection manager.
    await websocket.accept()
    try:
        # Loop indefinitely to listen for messages from the client.
        while True:

            while True:
                if (gpio.is_button_pressed()):
                    websocket.send_text("button_pressed")
                    break
                else:
                    continue

            data = await websocket.receive_text()
            ai_response: AIResponse = get_emotion_and_response(data)

            # Serve tea and finish chat when tea_type is specified
            if ai_response.tea_type:
                # TODO: Additional Improvements
                # milk: ai_response.milk_amount
                # sugar: ai_response.sugar_amount
                send_tea_command(f"serve_tea{ai_response.tea_type}")
                response_with_tea = f"{ai_response.response} お茶をどうぞ。"
                update_chat_prompt()

            else:
                response_with_tea = ai_response.response

            frontend_response = FrontendResponse(
                emotion=ai_response.emotion,
                response=response_with_tea,
                tea=ai_response.tea_type,
                sugar=ai_response.sugar_amount,
                milk=ai_response.milk_amount,
                finished=ai_response.finished
            )

            await websocket.send_text(frontend_response.model_dump_json())
    except Exception:
        print("error")
        # When the client disconnects, remove them from the connection manager.
