## Goal

Create a voice-interactive tea-serving robot that uses an LLM (like Gemini) to recognize user emotions and serve tea accordingly. The robot's program works on a Raspberry Pi 5 and uses Arduino for hardware control and Serial communication for interaction.
A panda avatar will appears on the screen and changes its acial expressions depending on what the user says.


## Flow

1. Talk with the user by voice using LLM like Gemini.
2. Recognize user's emotions and respond accordingly.
3. Select the type of tea that best suits the user's mood.
4. Serve the tea by controlling arduino with Serial communication.


## Requirements

- Panda avatar changes facial expressions by changing several images.
- Voice interaction using LLM like Gemini.
- There will be three types of tea and the types will be configurable through Web UI and stored in a toml file.


## Technologies

- HTML/CSS/JavaScript for the UI.
- Python(FastAPI) for backend logic and LLM integration.
