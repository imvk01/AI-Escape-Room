import re
from dataclasses import dataclass, replace


OPENING = (
    "You wake up in a locked library. There is a desk, a bookshelf, a painting "
    "with a word lock, a locked drawer, and an exit with a four-digit keypad."
)
WIN = "You escaped the library."
WORD = "openit"
CODE = "9742"


@dataclass(frozen=True)
class Game:
    frame_open: bool = False
    inventory: tuple[str, ...] = ()
    drawer_open: bool = False
    legend_read: bool = False
    strip_read: bool = False
    escaped: bool = False


def play(game, message):
    if game.escaped:
        return game, WIN

    action = " ".join(message.lower().split()).rstrip(".!?")
    action = re.sub(r"^(?:i (?:want to |would like to )?|please )", "", action)
    action = re.sub(r"\b(?:the|a|my) ", "", action)

    if action in {"inventory", "check inventory"}:
        return game, ", ".join(game.inventory) if game.inventory else "Your inventory is empty."

    inspection = re.fullmatch(
        r"(?:examine|inspect|read|look at|look inside) (desk|note|bookshelf|marked books|painting|frame|drawer|legend(?: card)?|strip|exit(?: door)?|door|keypad)",
        action,
    )
    if inspection:
        target = inspection[1]
        if target in {"legend", "legend card"}:
            if game.frame_open:
                return replace(game, legend_read=True), "Legend card\u2009—\u2009▲ = 7, ● = 2, ■ = 4, ★ = 9."
            return game, "You haven't uncovered the legend card."
        if target == "strip":
            if game.drawer_open:
                return replace(game, strip_read=True), "Keypad order, left to right\u2009—\u2009★ ▲ ■ ●."
            return game, "The drawer is locked."
        if target in {"desk", "note"}:
            return game, "The note says to read the first letter of each marked book, from top to bottom."
        if target in {"bookshelf", "marked books"}:
            return game, "From top to bottom you see Orchard, Pines, Embers, Night, Ivy, and Tides."
        if target in {"painting", "frame"}:
            return game, (
                "Behind the open frame are a brass key and a legend card."
                if game.frame_open and "brass key" not in game.inventory
                else "The frame is open. The legend card is behind it."
                if game.frame_open
                else "A word lock holds the painting's frame shut."
            )
        if target == "drawer":
            return game, "An order strip lies inside." if game.drawer_open else "The drawer has a keyhole."
        return game, "A four-digit keypad secures the exit."

    if action in {"take note", "pick up note"}:
        if "note" in game.inventory:
            return game, "The note is already in your inventory."
        return replace(game, inventory=(*game.inventory, "note")), "You put the note in your inventory."

    if action in {"take key", "take brass key", "pick up key", "pick up brass key"}:
        if "brass key" in game.inventory:
            return game, "The brass key is already in your inventory."
        if not game.frame_open:
            return game, "You haven't found a brass key."
        return replace(game, inventory=(*game.inventory, "brass key")), "You put the brass key in your inventory."

    if action in {"open drawer", "unlock drawer", "use key on drawer", "use brass key on drawer"}:
        if game.drawer_open:
            return game, "The drawer is already open. You can read the strip."
        if action.startswith("use ") and "brass key" in game.inventory:
            return replace(game, drawer_open=True), "The brass key opens the drawer. There is a strip inside."
        return game, "The drawer requires a brass key from your inventory. Try using it on the drawer."

    word = re.fullmatch(r"(?:enter|try|type) ([a-z]+) (?:on|into|at) (?:painting|frame|word lock)", action)
    if word:
        if game.frame_open:
            return game, "The frame is already open."
        if word[1] == WORD:
            return replace(game, frame_open=True), "The frame opens, revealing a brass key and a legend card."
        return game, "The word lock stays shut."

    code = re.fullmatch(r"(?:enter|try|type) ([0-9]{4})(?: (?:on|into|at) (?:keypad|exit|door|exit door))?", action)
    if code:
        if not (game.frame_open and game.drawer_open and game.legend_read and game.strip_read):
            return game, "Open both locks and read the legend card and strip before trying the keypad."
        if code[1] == CODE:
            return replace(game, escaped=True), WIN
        return game, "The keypad rejects the code. The exit stays locked."

    return game, "That action is unavailable. Try examining a room object or using an item you collected."
