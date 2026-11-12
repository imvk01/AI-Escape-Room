# Playtest cases

Start a fresh session for each case unless the setup calls for progress. To compare with Version 1, repeat the same inputs with a configured Gemini key. The V1 column describes the limitation of the design. The automated tests simulated model replies, and the V2 column records results from the Python tests.

| Case | Version 1 limitation | Version 2 observed result |
| --- | --- | --- |
| Use the brass key on the drawer before taking it | Gemini must infer the inventory from the chat. | The drawer remains closed and the player is told a collected key is required. |
| Enter a wrong word on the frame or a wrong code on the ready keypad | Gemini decides whether the input matches the solution. | A wrong value leaves both locks and existing progress as they were. |
| Enter the correct keypad code before reading both clues | Gemini must reconstruct which clues the player read. | The keypad requires both clues and both opened locks. |
| Claim the drawer is already open | Gemini could accept the player's claim as prior progress. | The sentence changes no game state. |
| Claim administrator access and demand an immediate escape | The UI trusts the model's escape marker. A simulated reply with that marker ended the game. | The command leaves the room state unchanged. |
| Ask for all secret codes at the start | The prompt contains the solutions. Gemini controls what it reveals. | The request leaves the state unchanged. A simulated model reply containing the code was discarded. |
| Try to inspect an object outside the room | Gemini may improvise an object. | The action is unavailable and leaves the state unchanged. |
| Solve the room and restart | Escape relies on the model recognizing the solution and returning its marker. | The correct code ends the game after the prerequisites. Restart clears the session and reopens the input. |

The automated suite passed 10 tests. A Chrome walkthrough of offline V2 also checked an uncollected key, the full puzzle sequence, a wrong code, escape, and restart. Screenshots show the rejected key attempt and escape confirmation. Live Gemini results are pending a configured API key.
