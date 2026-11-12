import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors

from v1.app import reply
from v2.game import Game, OPENING, WIN, play


load_dotenv(Path(__file__).with_name(".env"))
api_key = os.getenv("GEMINI_API_KEY")


def generate(contents, instruction):
    with genai.Client(api_key=api_key) as client:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"),
            contents=contents,
            config={"system_instruction": instruction, "max_output_tokens": 768},
        )
    return response.text or ""


def narrate(outcome):
    # Only display approved wording, and send Gemini just the current visible result.
    if not api_key:
        return outcome
    atmospheric = f"The library is quiet. {outcome}"
    try:
        choice = generate(
            f"Plain reply: {outcome}\nAtmospheric reply: {atmospheric}",
            "You are the Game Master. Return exactly one of the two approved replies, without its label.",
        ).strip()
        return atmospheric if choice == atmospheric else outcome
    except (errors.APIError, OSError, ValueError):
        return outcome


st.title("The Locked Library")
version = st.sidebar.radio("Game version", ("Version 1", "Version 2"))
state_key = version
if st.sidebar.button("Restart game") or state_key not in st.session_state:
    st.session_state[state_key] = {"history": [], "game": Game(), "escaped": False}

session = st.session_state[state_key]
history = session["history"]
game = session["game"]
st.write(OPENING)
st.caption("Describe one action at a time. Try “examine the bookshelf” or “read the note.”")
if version == "Version 2":
    st.caption("For locks, try “enter a word on the frame” or “enter a four-digit code on the keypad.”")
    st.sidebar.caption("Inventory")
    st.sidebar.write(", ".join(game.inventory) or "Empty")
elif not api_key:
    st.info("Add GEMINI_API_KEY to .env to play Version 1.")

if session["escaped"]:
    st.success(WIN)

for role, message in history:
    with st.chat_message("assistant" if role == "model" else "user"):
        st.text(message)

if not session["escaped"]:
    action = st.chat_input("What would you like to do?", disabled=version == "Version 1" and not api_key)
    if action and action.strip():
        action = action.strip()
        if version == "Version 1":
            try:
                answer, escaped = reply(generate, history, action)
            except (errors.APIError, OSError, ValueError):
                answer, escaped = "", False
            if not answer and escaped:
                answer = WIN
            if not answer:
                st.warning("The Game Master could not reply. Check your key, model, or quota and retry.")
                st.stop()
        else:
            session["game"], outcome = play(game, action)
            escaped = session["game"].escaped
            answer = narrate(outcome)
        history.extend([("user", action), ("model", answer)])
        session["escaped"] = escaped
        st.rerun()
