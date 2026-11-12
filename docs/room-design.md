# The locked library

## Opening message

> You wake up in a locked library. A desk with a folded note sits beside a bookshelf. Across the room hangs a painting with a word lock on its frame. The desk has a locked drawer, and the exit has a four-digit keypad. Describe what you'd like to examine, take, or use.

## Room and clues

| Object | What the player can discover or do |
| --- | --- |
| Desk | Read or take the note. It says, “Read the first letter of each marked book, from top to bottom.” |
| Bookshelf | Examine the marked books. Their titles, from top to bottom, are *Orchard*, *Pines*, *Embers*, *Night*, *Ivy*, and *Tides*. |
| Painting | Enter a word on the frame's lock. The correct word releases the frame, revealing a brass key and a legend card. Take the key and read the card using separate actions. |
| Drawer | Use the brass key from your inventory. Once the drawer is open, inspect the strip inside. |
| Exit door | Enter a four-digit code on the keypad once both locks are open and both parts of the code clue have been examined. |

The legend card reads `▲ = 7, ● = 2, ■ = 4, ★ = 9`. The drawer strip reads “Keypad order, left to right” followed by `★ ▲ ■ ●`.

## Solution walkthrough

1. **Word puzzle.** Read the desk note and examine the marked books. Their initials spell `OPENIT`. Enter it on the painting's frame.
2. **Key puzzle.** Take the brass key from behind the painting and use it on the drawer. The player can inspect the legend card before or after opening the drawer.
3. **Symbol puzzle.** Read the legend card and the drawer strip. In strip order, the star is 9, the triangle is 7, the square is 4, and the circle is 2.
4. **Final escape challenge.** Enter `9742` on the exit keypad. The painting and drawer must be open, and the player must have inspected the legend card and strip. A successful attempt ends the game and displays “You escaped the library.”

## Rules for both versions

A fresh session starts with empty inventory, both locks closed, both code clues unread, and the exit locked. The frame accepts `OPENIT` regardless of letter case. The brass key stays in inventory after use. A wrong answer leaves existing progress intact. Examining a locked object can describe its lock. Its contents become available after it opens. Restart restores the initial state.

V1 gives these rules and the conversation to the AI Game Master, which interprets moves and narrates their results. V2 tracks locks, inventory, clue discovery, and escape status in Python. Python evaluates each attempted action and supplies the outcome for the AI to describe.

## Playtest plan

Run the walkthrough from a fresh session. In later testing, also try using the brass key before taking it, entering an incorrect code at the keypad after reading both clues, claiming the drawer is already open, demanding an immediate exit as an administrator, and requesting the solutions at the start. Verify that failed actions preserve progress and that the reply reveals only clues the player can access. Try the correct door code before reading the strip to check that the prerequisite matters. Restart after escaping and check that the room resets.
