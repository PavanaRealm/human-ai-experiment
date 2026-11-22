# AI usage log

All prompts I sent to AI assistants for this project, in order, with the exact model and tool.
Where a prompt was a pasted terminal output or a screenshot, the entry says so in brackets instead of repeating the whole paste.

Tool for all entries so far: Claude (claude.ai, agent mode with file tools)
Model for all entries so far: Claude Sonnet 5.5 (model ID: claude-sonnet-5-5)

## 1. Step (a) – Plan (2026-11-19)
Attached file: technical-assessment-multi-participant-human-ai-experiment-platform-v4.md
Prompt:

~~~text
I am Pavani, a Master's student in AI at BTU Cottbus-Senftenberg (English C1, German A2). I was invited to a technical assessment for the Student Research Assistant - Full-Stack Developer job at the Center for Humans and Machines, Max Planck Institute for Human Development. The task file is attached. Please help me build it step by step.

DEADLINE: Reply to their email with a public GitHub repo link by Monday 23 November 2026 (hard limit Tuesday 24 November). The task is limited to 4 hours, so keep it minimal. I have a different important meeting on Friday 20 November at 11:00, so I will build on Saturday 21 and Sunday 22 November.

WHAT TO BUILD (from the task):
- Web app simulating a 3-participant group decision-making experiment. Participants are shown as Player A, B, C and must not know who is human or AI (blind condition).
- Waiting room: humans wait until all human slots are filled, then the experiment starts.
- 2 rounds of real-time text chat (about 1 minute each). They decide who becomes the Decision Maker. After each round everyone votes for one of the 3. After voting, show the final results and the selected Decision Maker. Intermediate feedback, tie-breaking and AI behaviour are my choice; document them briefly.
- config.yml sets participant types so they can test: 3 humans; 2 humans + 1 AI; 1 human + 2 AI. Also round count and round length.
- Stack: React frontend, Python FastAPI backend, MongoDB (my choice, or PostgreSQL), everything Dockerized and started with one command (docker compose up).
- Repo must contain: source code, config.yml, Docker setup, a short README (how to run, how to switch configs, key design decisions and trade-offs within the 4-hour limit), and an AI usage log (ai_prompts.md or ai_logs/) with ALL my prompts to AI assistants plus the exact model and tool names.
- Interview: 5-minute slide deck about my development process (how I broke down the problem, guided the AI, fixed issues, trade-offs), then run the app locally with Docker, demo the flow and discuss the code. They will ask how I built, structured and debugged it.

MY SKILLS AND GAPS (be honest about these):
- I know Python, Flask, React, Node.js, TypeScript, Git, SQL (from studies), Firebase/Firestore, and I have used the Gemini API (I built a tool-calling LLM agent: github.com/PavanaRealm/eo-agent).
- I have NOT used Docker, FastAPI, WebSockets or MongoDB before. Explain these simply when we meet them.
- I previously failed a live code debugging interview, so I need to understand every line.

HOW I WANT YOU TO WORK:
1. Short, plain English. Use short answers and simple words.
2. Build in small steps: (a) folder structure and config.yml, (b) backend with WebSockets and session logic, (c) AI players using the Gemini API, (d) React frontend, (e) Dockerfiles and docker-compose, (f) README, (g) tests and a final check. After each step, tell me exactly what to run and what I should see, and wait for my result.
3. Explain each part briefly after you write it so I can explain it in the interview. Keep the code small and clean; no extras like login or heavy styling.
4. Keep a running AI usage log. At the end of each step, give me the text to append to ai_prompts.md: my prompt, the model name, and the tool. Do not invent prompts; only log what I really asked. Tell me the exact model name you are.
5. Keep notes on every bug we hit and how we fixed it, because I need them for the 5-minute slide deck.
6. Never claim something works unless we have run it. Tell me plainly when something is a guess.
7. After the build, make a simple 5-slide outline for the presentation, and then act as the interviewer and ask me questions about my own code, including a bug you add on purpose that I must find and fix.

Start with step (a): propose the folder structure, the config.yml format and the session flow. Then wait for me.
~~~

## 2. Step (a) – follow-up 1 (2026-11-19)
~~~text
we will do this task on Sunday
~~~

## 3. Step (a) – follow-up 2 (2026-11-19)
~~~text
lets do half work tomorrow evening and another half on Sunday
~~~

## 4. Step (b) – start (2026-11-20)
~~~text
lets start doing it, I have not done anything
~~~

## 5. Step (b) – running it on my Mac (2026-11-20)
~~~text
(pasted my terminal output: cd human-ai-experiment/backend failed with "no such file or directory", and "python", "pip" and "pytest" were "command not found")
~~~

## 6. Step (b) – pip install error on my Mac (2026-11-20)
~~~text
(pasted my terminal output: pip install -r requirements.txt failed with "Could not find a version that satisfies the requirement fastapi==0.165.0", pip 21.2.4)
~~~

## 7. Step (b) – choosing a Python version (2026-11-20)
~~~text
(sent a screenshot of the python.org search results for "3.12.x", no text)
~~~

## 8. Step (b) – Python 3.13 release page (2026-11-20)
~~~text
(pasted the python.org release page text for Python 3.13.7, no question)
~~~

## 9. Step (b) – tests pass on my Mac (2026-11-20)
~~~text
(pasted my pytest output: 24 passed, 1 warning, Python 3.13.7 on macOS)
~~~

## 10. Step (b) – first run of fake_player (2026-11-20)
~~~text
(pasted my terminal output: ran fake_player.py, got only "joined, you: A")
~~~

## 11. Step (b) – fake_player connection error (2026-11-20)
~~~text
(pasted my terminal output: fake_player.py got "joined, you: A", then crashed with ConnectionClosedError: received 1012 (service restart))
~~~

## 12. Step (b) – typed config lines in the terminal (2026-11-20)
~~~text
(pasted my terminal output: I typed the YAML lines into the terminal by mistake, zsh errors; then python fake_player.py showed only "joined, you: A")
~~~

## 13. Step (b) – fake_player full run (2026-11-20)
~~~text
(sent 2 screenshots of my terminal: two fake_player.py runs, players A and B, both finished with a result, winner A)
~~~

## 14. Step (b) – pasted a note into the terminal by mistake (2026-11-20)
~~~text
(pasted my terminal output: I typed the bug-note text into the terminal by mistake, zsh "command not found" errors)
~~~

## 15. Step (b) – which bug note to save (2026-11-20)
~~~text
which bug note I should save
~~~

## 16. Step (b) – pasted the log entry into the terminal by mistake (2026-11-20)
~~~text
(pasted my terminal output: ran open -e on notes/bugs.md, then typed the log entry text into the terminal by mistake, zsh errors)
~~~

## 17. Step (b) – copy and first git push (2026-11-20)
~~~text
(pasted my terminal output: cp of ai_prompts.md worked, cp of bugs.md said "No such file or directory", git commit showed backend/which in the commit, git push failed with "Repository not found" because the URL still said YOUR-USERNAME)
~~~

## 18. Step (b) – looking for bugs.md in Downloads (2026-11-20)
~~~text
(pasted my terminal output: ls ~/Downloads | grep -i bugs printed nothing)
~~~

## 19. Step (b) – push worked (2026-11-20)
~~~text
(pasted my terminal output: git push succeeded, "main -> main"; then I pasted the bug note text into the terminal by mistake, zsh errors)
~~~

## 20. Step (b) – checking the repo state (2026-11-20)
~~~text
(pasted my terminal output: git status clean, git ls-files shows notes/bugs.md and no backend/which, grep count 1, git log shows one commit ebbf533 on main and origin/main)
~~~

## 21. Step (c) – files copied in (2026-11-20)
~~~text
(pasted my terminal output: git status --short listing 10 modified files and 2 new files; and the text ". it appeared")
~~~

## 22. Step (c) – the key (2026-11-20)
~~~text
I added the key and then saved , but then still it appeared
~~~

## 23. Step (c) – checking .env (2026-11-20)
~~~text
(pasted my terminal output of the env checks: ls shows .env and .env.example, git status shows only ?? .env.example, both grep counts 0)
~~~

## 24. Step (c) – file type and size of .env (2026-11-20)
~~~text
(pasted my terminal output: .env is ASCII text, 193 bytes, sed output with the value hidden)
~~~

## 25. Step (c) – line lengths of .env (2026-11-20)
~~~text
(pasted my terminal output: line lengths 68, 54, 68 and the text before the equals sign, "3:GEMINI_API_KEY=")
~~~

## 26. Step (c) – character check, first result (2026-11-20)
~~~text
(pasted my terminal output: grep -c for letters/digits only printed 0)
~~~

## 27. Step (c) – character check, second result (2026-11-20)
~~~text
(pasted my terminal output of the od -c check: the only unusual character in the value is one ".")
~~~

## 28. Step (c) – tests on my Mac (2026-11-20)
~~~text
(pasted my pytest output: 41 passed in 8.88s, Python 3.13.7, macOS)
~~~

## 29. Step (c) – uvicorn port error (2026-11-20)
~~~text
(pasted my terminal output: uvicorn failed with "[Errno 48] Address already in use")
~~~

## 30. Step (c) – first live run with Gemini (2026-11-20)
~~~text
(pasted the fake_player.py output of a full game on port 8001 with the real Gemini key: chat lines from B and C, round tallies, final result winner A)
~~~

## 31. Step (c) – first commit and push of step c (2026-11-20)
~~~text
(pasted my terminal output: git add, git status --short, git commit "Step c: Gemini AI players with speaking rules", git push main 78a226a)
~~~

## 32. Step (c) – port 8001 in use (2026-11-20)
~~~text
(pasted my terminal output: uvicorn with CONFIG_PATH=../config.test.yml on port 8001 failed with "[Errno 48] Address already in use")
~~~

## 33. Step (c) – second live run with Gemini (2026-11-20)
~~~text
(pasted my terminal output: the end of the uvicorn log with "AI players use Gemini model gemini-3.1-flash-lite", then the fake_player.py output of a full game on port 8001: chat from B and C, tallies, result winner A with tie_break last_round)
~~~

## 34. Step (c) – copied update 3, tests, second push (2026-11-20)
~~~text
(pasted my terminal output: rsync of step-c3, pytest 43 passed, config.yml back to defaults, git status showed 2 modified files, git commit and git push 80a8c41)
~~~

## 35. Step (c) – repo check on GitHub (2026-11-20)
~~~text
(sent a screenshot of my GitHub repo page, and pasted my terminal output: git log --oneline shows 4 commits, git ls-files shows config.test.yml)
~~~

## 36. Step (c) – decision to stop for tonight (2026-11-20)
~~~text
(answered the question "start step (d) now, or stop for tonight and continue on Sunday?" with: Stop, Sunday)
~~~
## 37. Cleaning up downloads (2026-11-20)
~~~text
ok , and we have downloaded so many files , can you remove all the unwanted files
~~~

## 38. Cleaning up downloads – list (2026-11-20)
~~~text
(pasted my terminal output: the ls -d list of files in ~/Downloads: zips, step-c folders, ai_prompts and bugs copies, the python pkg)
~~~

## 39. Cleaning up downloads – done (2026-11-20)
~~~text
(pasted my terminal output: ran the rm commands, ls -d printed "no matches found", git status printed nothing, ls shows the project files)
~~~

## 40. Step (d) – start (2026-11-22)
~~~text
start(d)
~~~

## 41. Step (d) – waiting room screenshot (2026-11-22)
~~~text
(sent a screenshot of the waiting room: "You are Player A")
~~~

## 42. Step (d) – chat screenshot (2026-11-22)
~~~text
(sent a screenshot of the chat screen: a message from Player C written by Gemini, 21 s countdown)
~~~

## 43. Step (d) – result screenshot (2026-11-22)
~~~text
(sent a screenshot of the result screen: Player C is the Decision Maker, totals A 0, B 0, C 4)
~~~

## 44. Step (d) – votes were 0 (2026-11-22)
~~~text
I did not clicked anything , it just happened after few seconds
~~~

## 45. Step (d) – backend not running (2026-11-22)
~~~text
(pasted my terminal output: `npm run dev` run inside the backend folder gave ENOENT package.json) after pressing on those links both are showing , connections lost
~~~

## 46. Step (d) – backend log (2026-11-22)
~~~text
(pasted my terminal output: uvicorn started on port 8000, with two 404 lines for "GET /" and "GET /favicon.ico")
~~~

## 47. Step (d) – two-tab result, 2 votes per round (2026-11-22)
~~~text
(sent 2 screenshots of the result screens of both tabs: Player B is the Decision Maker, tie over all rounds, round 1: A 2 B 0 C 0, round 2: A 0 B 2 C 0)
~~~

## 48. Step (d) – answers to my questions (2026-11-22)
~~~text
Did your chat messages show up in the other tab? yes,  Did you see the vote buttons turn blue after clicking in each tab?yes
~~~

## 49. Step (d) – two-tab result, 3 votes per round (2026-11-22)
~~~text
(sent 2 screenshots of the result screens of both tabs: Player C is the Decision Maker, round 1: A 0 B 0 C 3, round 2: A 0 B 0 C 3)
~~~

## 50. Step (d) – committed and pushed, then Docker check (2026-11-22)
~~~text
(pasted my terminal output: git add, git status --short, git commit "Step d: React frontend", git push (80a8c41..43e20a7), then `docker --version` / `docker run hello-world` gave "command not found: docker", node --version v26.4.0)
~~~

## 51. Step (e) – Docker not found again (2026-11-22)
~~~text
(pasted my terminal output: docker --version, docker run hello-world and docker compose version all gave "command not found: docker")
~~~

## 52. Step (e) – Docker Desktop welcome screen (2026-11-22)
~~~text
(sent a screenshot of the Docker Desktop "Welcome to Docker" sign-in screen)
~~~

## 53. Step (e) – Docker Desktop running (2026-11-22)
~~~text
(sent a screenshot of Docker Desktop with "Engine running" at the bottom left)
~~~

## 54. Step (e) – Docker works (2026-11-22)
~~~text
(pasted my terminal output: Docker version 29.9.3, "Hello from Docker!" (arm64v8), Docker Compose version v5.7.0)
~~~

## 55. Step (e) – ran only the last command (2026-11-22)
~~~text
(pasted my terminal output: `docker compose exec mongo mongosh ...` gave "command not found: docker")
~~~

## 56. Step (e) – port 5173 already in use (2026-11-22)
~~~text
(pasted my terminal output: "Error response from daemon: ports are not available: exposing port TCP 0.0.0.0:5173 ... address already in use", then countDocuments printed 0)
~~~

## 57. Step (e) – containers started (2026-11-22)
~~~text
(pasted my terminal output: mongo, then backend log lines "AI players use Gemini model", "Finished sessions are saved to MongoDB", "Uvicorn running on http://0.0.0.0:8000")
~~~

## 58. Step (e) – old terminal window (2026-11-22)
~~~text
(pasted my terminal output: in an old window `docker compose exec ...` gave "command not found: docker")
~~~

## 59. Step (e) – empty database result (2026-11-22)
~~~text
(pasted my terminal output: docker --version worked in a new window, `db.sessions.find().toArray()` printed [], then the export PATH command)
~~~

## 60. Step (e) – asked if the game was finished (2026-11-22)
~~~text
Did you finish the game in the browser before this? yes
~~~

## 61. Step (e) – Docker game result screenshots (2026-11-22)
~~~text
(sent 2 screenshots of both tabs' result screens: Player A is the Decision Maker, round 1 A 3 B 0 C 0, round 2 A 1 B 0 C 2)
~~~

## 62. Step (e) – saved game in MongoDB (2026-11-22)
~~~text
(attached a text file with my terminal output: logs, countDocuments printed 1, and the saved document from `db.sessions.find().toArray()`)
~~~

## 63. Step (e) – docker compose down, commit, push (2026-11-22)
~~~text
(pasted my terminal output: docker compose down, git status --short, git commit "Step e: Docker, docker-compose and MongoDB", git push (43e20a7..aad4766))
~~~

## 64. Step (f) – committed and pushed the README (2026-11-22)
~~~text
(pasted my terminal output: git status --short, git commit "Step f: README", git push (aad4766..b3236cf))
~~~

## 65. Step (g) – fresh clone test (2026-11-22)
~~~text
(pasted my terminal output: in /tmp/clone-test, `docker compose up -d`, `docker compose restart backend`, then `docker compose down -v` and rm -rf; no results of the games)
~~~

## 66. Step (g) – "ok" (2026-11-22)
~~~text
ok
~~~

## 67. Step (g) – I pasted the checklist text back (2026-11-22)
~~~text
Send me the results before you clean up. Use this checklist: sorry I forgot
~~~

## 68. Step (g) – same again (2026-11-22)
~~~text
Send me the results before you clean up. Use this checklist: sorry I forgot
~~~

## 69. Step (g) – fresh clone log (2026-11-22)
~~~text
(attached a text file with my terminal output of `docker compose up --build` in the fresh clone: images built, mongo and nginx started, backend warning "GEMINI_API_KEY is not set -> using the placeholder AI", "Uvicorn running on http://0.0.0.0:8000")
~~~

## 70. Step (g) – round 1 feedback screenshot (2026-11-22)
~~~text
(sent a screenshot of the round 1 feedback screen: A 2 votes, B 0, C 1, "The next round starts soon.", 2 s)
~~~

## 71. Step (g) – game finished, no screenshot (2026-11-22)
~~~text
Done with both of the screens, but I didn't got time to take a screenshot of the other screen because only 2 seconds was left when I was trying to take a screenshot. So and then it gone, but it's the result came.
~~~

## 72. Step (g) – config switch (2026-11-22)
~~~text
(pasted my terminal output: `open -e config.yml` twice, then `docker compose restart backend`)
~~~

## 73. Step (g) – game with one tab, second tab refused (2026-11-22)
~~~text
(sent 2 screenshots: a round 1 feedback screen "Player A (you): 1 vote, Player B: 2 votes, Player C: 0 votes", and the screen "Sorry, an experiment is already running.")
~~~

## 74. Step (g) – config line (2026-11-22)
~~~text
(pasted my terminal output: `grep participants config.yml` printed "participants: [human, ai, ai]")
~~~

## 75. Step (g) – public repo check (2026-11-22)
~~~text
(sent 2 screenshots of the GitHub repo page in an incognito window: Public, 7 commits, no .env in the file list, README displayed)
~~~

## 76. Step (g) – tests on my Mac (2026-11-22)
~~~text
(pasted my terminal output: pytest 48 passed; npm test: 2 files, 17 tests passed)
~~~
