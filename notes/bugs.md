# Bug notes (for the 5-minute slide deck)

Only things that really happened. Add new ones as they come, with: what I saw, the cause, the fix.

## Step (b) – backend

No real bugs hit in this step. All 25 tests passed on the first run.

What I did to check the tests are not "always green" (mutation check): I broke the code on purpose and ran the tests.
- Voting never ends early -> 7 tests failed (timeouts). Good.
- Removed the "someone left during the waiting room timer" check -> 1 test failed. Good.
- Allowed chat in any phase -> 1 test failed. Good.
Then I restored the code and all tests passed again.

Design risks I thought about BEFORE writing code (these were avoided by design, not bugs I hit):
- The player must get "joined" (their letter) before the first "phase" message -> `maybe_start()` is called after "joined" is sent.
- A human leaves while the waiting-room timer runs -> the experiment must not start with a missing player -> re-check after the timer.
- A background task that crashes fails silently in asyncio -> `run()` has try/except with logging.

## Later steps

### Bug 1: pip could not find fastapi==0.165.0 (Mac)
- Saw: "No matching distribution found for fastapi==0.165.0". pip (version 21.2.4) only offered FastAPI up to 0.128.8.
- Cause: the Mac's default Python was too old for the pinned FastAPI (version not checked; pip 21.2.4 suggests the old system Python). The AI built and tested on Python 3.13 and only guessed that other versions would work.
- Fix: the AI first suggested Python 3.12, but on python.org 3.12 is security-only and has no Mac installer. Installed Python 3.13.7 instead and recreated the virtual environment. After that: 24 tests passed on my Mac.
- Lesson: "works on the AI's machine" is not "works on mine". The README now needs to say which Python version is required.

### Note 2: fake_player crashed with "1012 (service restart)"
- Saw: after "joined", the player crashed with ConnectionClosedError 1012.
- Cause: not confirmed. Most likely the server (uvicorn --reload) was restarted while the player was connected, since 1012 is what a stopping server sends. A second run worked fine.
- Fix: none needed in the experiment code. Known limitation: fake_player prints a long error when the server stops.

### Problem 3: the stub AI chats too much (found in step b, fixed in step c)
- Saw: in a real 2-human run the stub AI player sent more than 10 messages per 60-second round and repeated the same lines.
- Why it matters: a real person would not do that, so it would reveal the AI and break the blind condition.
- Fix: speaking rules in session.py (AI waits 4-10 s, at most 3 messages per round, never two messages in a row), set in config.yml. Checked on a real server run: each AI wrote exactly 3 messages per round. Unit test + 2 deliberate-break checks (no cap / allow double messages) both made the test fail.

### Mistake 4: pasting notes into the terminal ran them (junk file "which" committed)
- Saw: `git commit` listed `backend/which`. Later, text with backticks in it printed "no such file or directory: backend/which".
- Cause: I pasted note text into the terminal instead of a file. A line starting with ">" redirected output into a new file called "which". Backticks make the shell run the command inside them (`git commit` ran by accident).
- Fix: `git rm -f backend/which`, amended the commit before the first push, then checked with `git status`, `git ls-files`, `git log`. The AI then switched to sending finished files instead of text to paste.
- Lesson: check `git status` before committing; paste notes into a file, never into the terminal.

### Problem 5: first live Gemini run (step c): it works, but the AI is easy to spot
- Setup: real key, model gemini-3.1-flash-lite, 1 human (terminal bot) + 2 AI. It worked: the model name was accepted, both AIs chatted, both voted, the game finished.
- Saw (from the real output):
  - After only ONE human message, an AI wrote that "B seems really organized with the tasks so far" and another said C "has been keeping us on track". Nothing like that had happened: the model made up context.
  - Messages were 25-40 words, very polite, and often ended with "What do you think about that?".
  - Round 1: AI player B argued for C and then for A in the chat, but the round tally ({'A': 1, 'B': 2, 'C': 0}) means both AIs voted B. Either B really voted for itself, or its answer was unclear and the random fallback was used. I could not tell, because nothing was logged for that case.
- Fix (a guess until it is run again): prompt now says "you only know what is written in the chat", "under 25 words", "do not end every message with a question", and for votes "stay consistent with what you said". Unclear vote answers now write a warning to the log.
- Also added: config.test.yml, so quick tests do not need edits to config.yml.
- Second live run after the prompt change (one run only):
  - Better: no more "so far" / "keeping us on track" made-up context; messages about 15-25 words; fewer questions; round 1 votes matched the chat (B suggested C, C accepted, both AIs voted C).
  - Still not perfect: an AI said "I've done a few tasks like this before" (an invented personal claim) and talked about "the next part"; messages are still very agreeable and polite.
  - Round 2: B and C both said "stick to the plan" (= C), but the tally {'A': 2, 'B': 0, 'C': 1} shows one AI voted A. I did not check the log for an "unclear vote" warning, so I do not know if that was the random fallback or the model.
  - Tie-break worked as designed: totals A 3, C 3 -> tie -> winner A by the last round (A had 2 votes in round 2).
  - Decision: stop tuning the prompt here (time limit). Listed as a limitation in the README.

### Test of failure: Gemini unreachable (step c)
- Setup: real server, a fake API key, so every Gemini call failed (in my AI's sandbox the network is blocked, 17 errors).
- Saw: the game still finished with a result. The AIs stayed silent in chat and voted randomly. The server log filled with 17 long stack traces.
- Fix: log one short warning line per failure instead of a full trace.
- Limit (documented, not fixed): if Gemini is down the whole game, the AI players never speak, which would reveal them. A real study should check the log after each session.

## Step (d) – frontend

### Bug 7: the page went blank when the first chat message arrived (found only in a real browser)
- Saw: in a real Chrome run with two tabs, both tabs turned completely white right after one tab sent a chat message. Console: "l is not a function" (minified build). With the unminified dev server: "An effect must not return anything besides a function ... destroy is not a function".
- Cause: my effect that scrolls the chat to the newest message was written as `useEffect(() => bottom.current?.scrollIntoView?.(...), [...])`. The arrow function returns whatever `scrollIntoView` returns. In this Chrome that is a Promise, and React tried to call it as the cleanup function, which crashed the whole page.
- Why the tests did not catch it: all 16 frontend tests passed. They run in a fake browser (jsdom) that has no `scrollIntoView`, so the effect returned undefined there.
- Fix: write the effect with braces so it returns nothing. Added a test where `scrollIntoView` returns a Promise. Checked that the new test FAILS with the old code and passes with the fix.
- Lesson: unit tests in a fake browser are not enough. Run the real thing in a real browser.

### Frontend checks done
- 17 frontend tests (state logic + whole UI against a fake server). 4 deliberate-break checks (input not cleared, old rounds' messages not filtered, the word "human" on the waiting screen, lost connection ignored): each made a test fail.
- Real Chrome, real backend, 2 browser tabs as 2 humans (+1 placeholder AI): waiting room, chat between tabs, vote, round feedback, round 2 starts with an empty chat, result, and a new visitor after the game gets a fresh waiting room. No browser errors. No word like "AI" or "human" on any screen.
- NOT checked by me: a real game on the user's Mac with the real Gemini key through the browser.

## Step (d) – testing on a Mac, two tabs

### Not a bug 8: "connection lost" in both tabs
- Saw: both tabs showed "connection lost" although the page loaded.
- Cause: I had stopped the backend with `pkill` and not restarted it. The frontend (a separate process) was still running, so the page loaded, but the WebSocket on port 8000 had nobody to talk to. Also `npm run dev` was typed inside `backend/` and failed with ENOENT (no package.json there).
- Fix: start `uvicorn` in `backend/` and `npm run dev` in `frontend/`. Two processes, two terminals.
- Lesson: the "connection lost" screen did what it should. It is also what a reviewer sees if the backend is down.

### Not a bug 9: 2 votes per round instead of 3
- Saw (15 s vote time, 2 human tabs + 1 AI): round 1 A 2 B 0 C 0, round 2 A 0 B 2 C 0. Each round had only 2 votes.
- Cause: not confirmed. The most likely reason is a missed click inside the 15 s while switching tabs (non-voters count as abstain, by design). With `vote_seconds` 30 and clicks in both tabs: 3 votes per round (A 0 B 0 C 3 in both rounds). I did not read the backend log for the first run, so the missed click is a guess.
- Also confirmed: the tie-break works (A 2 + B 2 tied, the last round decided: B).
- Change: default `vote_seconds` 15 -> 30, because 15 s is too short with two tabs.
- Found while reading the code: a player can vote for themselves (the server only checks that the target is A, B or C). Kept, and noted in the README.

## Step (e) – Docker and MongoDB
- db.py: own small version (`Store.save_session`, `make_store()` from `MONGO_URL`). Tests with a fake collection; 2 deliberate-break checks (hook not called; DB error not caught): each made a test fail.
- NOT checked by me: the Dockerfiles and docker-compose.yml. My AI's sandbox has no Docker engine and no MongoDB, so I only ran `docker compose config` (syntax). The first real run was on the user's Mac.

### Step (e) – mistakes while testing in Docker (all my own, none in the code)
- `docker: command not found` three times: a terminal window opened before Docker Desktop was installed does not know the command. Fix: open a new window (or `export PATH="$PATH:/Applications/Docker.app/Contents/Resources/bin"`).
- "address already in use" on port 5173 when running `docker compose up`: my old `npm run dev` was still running. Fix: stop it (`pkill -f vite`) and check with `lsof -i :5173 -i :8000`. Same kind of problem as the earlier uvicorn port 8000 problem. Mentioned in the README.
- `db.sessions.find()` printed `[]`: I ran it before the game reached the result screen. A session is saved only when the game finishes. After the result screen: count 1 and the full record (participants, messages, votes, round tallies, result).
- Docker run, 2 tabs (2 humans + 1 AI, real Gemini): all 3 votes counted in both rounds, the result matched the saved record.

## Step (g) – final checks (2026-11-22)
- Fresh `git clone` of the public repo into /tmp, no `.env`, `docker compose up --build`: all 3 containers start. The backend prints "GEMINI_API_KEY is not set -> using the placeholder AI" and does not crash. A full game with 2 tabs reached the result screen (round 1 feedback seen: A 2, B 0, C 1 = 3 votes; I saw the final result screen myself but did not get a screenshot).
- Config switch: edited `config.yml` in the clone to `[human, ai, ai]`, `docker compose restart backend`, ONE tab: the game started by itself and ran with 1 human + 2 AI (round 1: A 1, B 2, C 0 = 3 votes). A second tab was refused with "Sorry, an experiment is already running." (the designed screen). So the README instruction "edit config.yml, then `docker compose restart backend`" works (config line checked with grep).
- Mistake of mine: I pasted the checklist instructions back into the chat instead of filling it in; I also cleaned up the test folder before sending results, so the first run had to be repeated.
- Tests on my Mac: 48 backend, 17 frontend passed.
- Repo checked in a private browser window: public, README shown, no `.env` in the file list.
