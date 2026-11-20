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
