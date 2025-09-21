# Tea-Serving Robot

This project is a voice-interactive tea-serving robot that uses a Large Language Model (LLM) to recognize user emotions and serve a tea that matches their mood. The robot is controlled by a Raspberry Pi 5, with an Arduino for hardware control.

## Architecture

The system is composed of three main parts:

1.  **Frontend (Web UI):** A web-based interface for user interaction, displaying a panda avatar, and for configuration.
2.  **Backend (Python/FastAPI):** The core application logic running on the Raspberry Pi, handling voice processing, LLM interaction, emotion recognition, and hardware control.
3.  **Arduino:** The microcontroller responsible for the physical actions of the robot.

```
+-----------------+      +----------------------+      +-----------------+
|      User       |      |      Frontend        |      |     Backend     |
| (Voice & Click) | <--> | (HTML/CSS/JS)        | <--> | (Python/FastAPI)|
+-----------------+      +----------------------+      +-----------------+
                         | - Panda Avatar       |      | - LLM Integration|
                         | - Voice Input/Output |      | - Emotion Logic  |
                         | - Config UI          |      | - Tea Selection  |
                         +----------------------+      +-----------------+
                                                             | (Serial)
                                                             v
                                                       +-----------------+
                                                       |     Arduino     |
                                                       | (Hardware Ctrl) |
                                                       +-----------------+
```

## File Structure

```
/teaserver
├── backend/
│   ├── main.py         # FastAPI app, WebSocket, and config endpoints
│   ├── llm.py          # Gemini LLM integration and emotion analysis
│   ├── arduino.py      # Serial communication with Arduino
│   └── config.py       # Logic to handle the TOML config file
├── frontend/
│   ├── index.html      # Main page with the panda avatar
│   ├── config.html     # Web UI for configuring tea types
│   ├── css/
│   │   └── style.css   # Styles for both pages
│   └── js/
│       ├── main.js     # Handles voice recognition, synthesis, and avatar changes
│       └── config.js   # Handles fetching/updating tea configuration
├── arduino/
│   └── tea_robot.ino   # Arduino code to control motors/servos
└── config.toml         # File to store tea types and their associated emotions
```

## How to Run

1.  **Install Poetry:** (If not already installed) `pip install poetry`
2.  **Install dependencies:** `poetry install`
3.  **Set up the environment:** Create a `.env` file in the root directory and add your Gemini API key: `GEMINI_API_KEY=YOUR_API_KEY`
4.  **Run the backend:** `poetry run uvicorn backend.main:app --reload`
5.  **Open the frontend:** Open `frontend/index.html` in a web browser.
6.  **Configure teas:** Open `frontend/config.html` to change the tea selection.
7.  **Upload to Arduino:** Upload the `arduino/tea_robot.ino` sketch to your Arduino.


## Future Improvements

- Enable to change Arudino settings such as the amount of water from the web UI.
- Allowing the AI to determin tea brewing time.
