# AI Web Automation Agent

This project is an AI-powered web automation agent that interprets and executes natural language commands to perform tasks on websites (e.g., Amazon, Netflix, YouTube).

## Features
- Open specified websites and perform actions (search, add to cart, play video, etc.)
- Natural language understanding (NLU) to extract actionable tasks (local, no paid API required)
- Browser automation using Playwright
- Secure credential management for logins (Amazon)
- CLI, GUI, and Voice interfaces
- Robust error handling and flexible command phrasing

## Setup
1. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   playwright install
   python -m spacy download en_core_web_sm
   ```
   For voice interface:
   ```
   pip install SpeechRecognition pyttsx3 pyaudio
   # On Windows, you may need to install PyAudio wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
   ```

## Usage
### CLI
Run the main agent loop:
```
python main.py
```

### GUI
Run the graphical interface:
```
python gui.py
```

### Voice Interface
Run the voice interface (requires microphone):
```
python voice.py
```

## Example Commands
- Go to Amazon, search for a wireless mouse under $80, and add the first one to the cart.
- Go to Netflix and play the movie Titanic.
- Go to YouTube and play a video titled Python tutorial for beginners.
- Search for headphones on Amazon below $50 with at least 4 stars.

## Supported Sites
- Amazon (search, add to cart, login)
- YouTube (search and play video)
- (Netflix NLU supported, automation can be added)

## Optional Add-ons
- Voice command interface (included)
- GUI interface (included)
- Error recovery and advanced filters

## Notes
- Credentials for Amazon are stored securely using the `keyring` library.
- Playwright launches a visible browser window for automation.
- NLU is local and does not require OpenAI or paid APIs. 