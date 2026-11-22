# Human / AI group decision experiment

A small web app that simulates a blind group experiment. Three players (Player A, B, C) chat for two rounds, vote on who should be the **Decision Maker**, and see the result. Depending on the config, some players are humans and some are AI (Gemini). Nobody is told which is which.

Stack: React (Vite) · Python FastAPI + WebSockets · MongoDB · Docker Compose.

## Run it

You need Docker Desktop. One command:

```
cp .env.example .env     # then put your Gemini API key after GEMINI_API_KEY=
docker compose up --build
```

Open **http://localhost:5173**. Open one browser tab per human player (2 tabs with the default config). The game starts when all human slots are filled.

- Without a Gemini key the app still runs. The AI players then use a simple placeholder that writes canned messages, and the backend log prints a warning. Real AI behaviour needs the key.
- `.env` is in `.gitignore`. Never commit a key.
- Ports 5173 (web), 8000 (backend) and MongoDB inside Docker are used. Stop anything else on 5173 and 8000 first.
- Stop with Ctrl+C, then `docker compose down` (saved sessions stay in a Docker volume).

## Switch the condition (`config.yml`)

```yaml
participants: [human, human, ai]   # Player A, B, C
rounds: 2
chat_seconds: 60
vote_seconds: 30
feedback_seconds: 8
min_wait_seconds: 3
```

| Condition | `participants` | Tabs to open |
|---|---|---|
| 3 humans | `[human, human, human]` | 3 |
| 2 humans + 1 AI | `[human, human, ai]` | 2 |
| 1 human + 2 AI | `[human, ai, ai]` | 1 |

The file is read once at startup. After editing it run `docker compose restart backend` (it is mounted into the container, no rebuild needed). The AI settings (model, reply delay, max messages per round) are in the same file.

## Saved data

Each finished game is saved to MongoDB (database `experiment`, collection `sessions`): participants, full chat log, every vote, round tallies and the result.

```
docker compose exec mongo mongosh experiment --eval "db.sessions.find().toArray()"
```

## How a game works

1. **Waiting room.** Shown until every human slot is filled, and at least `min_wait_seconds`. It shows no counts and no "waiting for AI" text.
2. **For each round:** chat (`chat_seconds`) → vote (`vote_seconds`, ends early when everyone voted) → feedback (`feedback_seconds`).
3. **Result.** The Decision Maker, total votes and votes per round.

## Design decisions

- **Blind condition.** The server never sends who is human or AI. The screens never use the words "human", "AI" or "bot". Player letters are fixed per slot; the human always gets the first free human slot.
- **The server owns the game.** Phases and timers run on the server. The browser only shows a countdown, so tabs cannot get out of sync and a client cannot cheat on time.
- **Feedback between rounds:** the vote count per player for that round only. It does not say who voted for whom, because that could identify the AI voters.
- **Winner rule:** most votes over all rounds. Tie → most votes in the last round. Still tied → random. Players may vote for themselves. Someone who does not vote in time counts as abstaining.
- **Plain WebSockets, one endpoint (`/ws`).** Chat and votes need push messages in both directions. The messages are small JSON objects (see `backend/app/session.py`).
- **AI behaviour.** Gemini gets a short persona prompt: casual, under 25 words, only knows what is in the chat, deflects questions about being an AI. An AI waits 4–10 s before writing, writes at most 3 messages per round, and never writes twice in a row. This keeps it from flooding the chat and from being recognisable by speed. For voting it is asked to stay consistent with what it said in the chat.
- **If Gemini fails** (no network, quota, bad answer): the AI stays silent in the chat and votes randomly. The game always finishes. The cost is that a silent AI would be noticeable.
- **MongoDB is only for finished sessions.** The live game state is in memory, which is simple and fast. A database call that fails is logged and does not break the game.
- **Config is plain YAML**, checked at startup (3 players, at least 1 human, valid timers), with a clear error message.

## Trade-offs and known limitations (4 hour limit)

- **No reconnect.** Refreshing the page in a running game loses the player's slot. If all humans leave, the game stops.
- **One live game at a time.** A new game starts after the previous one ended. No lobbies or multiple parallel groups.
- **AI realism is limited.** The messages are polite and agreeable, and the model sometimes makes small claims about itself ("I've done tasks like this before"). I stopped tuning after two live tests. A real study would need more prompt work and checks.
- **Backend log is the only check for Gemini failures.** After a session, look at the log for "failed" warnings. There is no dashboard.
- **The browser connects directly to port 8000** (`ws://<host>:8000/ws`). Fine for localhost; a real deployment would put both behind one reverse proxy. Override with `VITE_WS_URL` when building.
- **No authentication, no rate limits.**
- **Ethics.** This deceives participants about who is a human. A real study would need informed consent beforehand and a debriefing afterwards. Not built.

## Development without Docker

Needs Python 3.13 and Node 22 or newer.

```
# backend (terminal 1)
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload            # http://localhost:8000

# frontend (terminal 2)
cd frontend
npm install
npm run dev                              # http://localhost:5173
```

Without `MONGO_URL` set, finished sessions are not saved (the log says so). The key is read from `.env` in the repo root.

## Tests

```
cd backend && pytest -q                  # winner rule, 3 conditions, waiting room, AI rules, WebSocket, DB hook
cd frontend && npm test                  # state logic and the whole UI against a fake server
```

Quick manual tests without the browser:

```
cd backend
CONFIG_PATH=../config.test.yml uvicorn app.main:app --port 8001      # 1 human + 2 AI, short timers
python fake_player.py ws://localhost:8001/ws                          # a terminal bot acting as the human
```

## Layout

```
config.yml            experiment settings (the 3 conditions)
docker-compose.yml    mongo + backend + frontend
backend/app/          main.py (WebSocket endpoint) · session.py (game logic) · ai_player.py (Gemini)
                      config.py · db.py (MongoDB)
backend/tests/        pytest
frontend/src/         game.js (state + WebSocket) · Screens.jsx · App.jsx · tests
ai_prompts.md         every prompt I gave the AI assistant, with model and tool
notes/bugs.md         bugs and mistakes found while building
```

## AI usage

See `ai_prompts.md`: all my prompts, the model (Claude Sonnet 5.5, `claude-sonnet-5-5`) and the tool (Claude, claude.ai agent mode with file tools). The experiment's AI players use Gemini (`gemini-3.1-flash-lite`).
