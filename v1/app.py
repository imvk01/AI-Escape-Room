from pathlib import Path


ROOM_DESIGN = Path(__file__).resolve().parents[1] / "docs" / "room-design.md"
ESCAPE_MARKER = "[ESCAPED]"


def instructions():
    return (
        "You are the Game Master. Narrate the locked library in two or three short sentences. "
        "Use the conversation history to track actions, locks, inventory, and clues. "
        "Reveal clues only when the player performs the appropriate action. "
        "The following design is private. Follow the walkthrough and rules. "
        f"End your reply with {ESCAPE_MARKER} only when the player meets all door prerequisites "
        "and enters the correct code.\n\n"
        + ROOM_DESIGN.read_text().split("## Playtest plan")[0]
    )


def reply(generate, history, action):
    contents = [
        {"role": role, "parts": [{"text": message}]}
        for role, message in [*history, ("user", action)]
    ]
    answer = generate(contents, instructions()).strip()
    return answer.removesuffix(ESCAPE_MARKER).strip(), answer.endswith(ESCAPE_MARKER)
