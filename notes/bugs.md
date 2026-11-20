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

### Observation (not a crash): the stub AI chats too much
- Saw: in a real 2-human run the stub AI player sent about 15 messages per 60-second round and repeated the same lines.
- Why it matters: a real person would not do that, so it would reveal the AI and break the blind condition.
- Plan: step (c) makes the AI reply less often and react to what others write, then check it in a real run.
