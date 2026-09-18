# Multi-Agent Educational Chatbot — Modern Frontend

This version replaces only the Gradio presentation layer with a responsive HTML/CSS/JavaScript interface.

## Architecture

Browser
→ `POST /chat`
→ existing `route_question()`
→ Manager Agent
→ Study / Coding / General Agent
→ existing Groq LLM configuration
→ response
→ browser

## Files

- `app.py` — existing AI/agent logic plus the minimal Flask API/serving layer
- `templates/index.html` — frontend structure
- `static/style.css` — responsive UI
- `static/script.js` — chat interaction and API communication
- `requirements.txt` — runtime dependencies

## Render

Use a Python web service with a start command such as:

`python app.py`

The application reads Render's `PORT` environment variable and binds to `0.0.0.0`.

Set `GROQ_API_KEY` in Render Environment Variables. Never put the key in source code.
