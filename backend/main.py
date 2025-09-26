from .llm import AIResponse
import os
from .arduino import send_tea_command
from .llm import get_emotion_and_response, update_chat_prompt
from .config import get_tea_config, save_tea_config
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from . import gpio

# Manages active WebSocket connections and allows broadcasting messages to all clients.


class ConnectionManager:
    def __init__(self):
        # A list to store active WebSocket connections.
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Accepts a new WebSocket connection and adds it to the list of active connections.
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Removes a WebSocket connection from the list of active connections.
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Sends a message to all active WebSocket connections.
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


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
    await manager.connect(websocket)
    try:
        # Loop indefinitely to listen for messages from the client.
        while True:
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
        # When the client disconnects, remove them from the connection manager.
        manager.disconnect(websocket)

# This function is called when the GPIO button is pressed.


async def button_pressed_callback():
    # Broadcast a 'button_pressed' message to all connected clients.
    await manager.broadcast("button_pressed")

# This function runs when the FastAPI application starts.


@asynccontextmanager
async def lifespan(app: FastAPI):
    gpio.setup_button_callback(button_pressed_callback)
    yield
    pass
