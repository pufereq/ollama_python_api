# -*- coding: utf-8 -*-

import logging as lg

import flask

from ollama_python_api import OllamaAPI

lg.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create a Flask app
app = flask.Flask(__name__)

# Load the system prompt from a file
with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()

# Initialize the OllamaAPI object
api = OllamaAPI(system_prompt=system_prompt, debug=True)


@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint for interacting with the chatbot.

    This endpoint accepts a POST request with a JSON body containing a session ID and a message.
    The chatbot will respond with a message.
    """
    data = flask.request.json
    if data["session_id"] not in api.history:
        return flask.jsonify(
            {
                "error": "Invalid session ID, please get a new session ID (/new_session_id)"
            }
        )

    try:
        session_id = data["session_id"]
        text = data["message"]
    except (KeyError, TypeError):
        return flask.jsonify({"error": "Invalid request format"})

    response = api.chat(session_id, text)
    return flask.jsonify(response)


@app.route("/new_session_id", methods=["GET"])
def new_session_id():
    """
    New session ID endpoint for generating a new session ID.

    This endpoint accepts a GET request and returns a new session ID.
    """
    session_id = api.generate_session_id()
    return flask.jsonify({"session_id": session_id})
