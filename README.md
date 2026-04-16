# Game Dev Crew

A **CrewAI multi-agent system** that turns a one-line game idea into a fully playable **Pygame script** — automatically. Three specialised AI agents collaborate in a sequential pipeline: designer → developer → QA reviewer.

---

## How It Works

```
Your idea: "A fun endless runner where a character jumps over obstacles"
        │
[Agent 1] Creative Game Designer
        └── Produces a Game Design Document (GDD)
                │
        [Agent 2] Senior Python Game Developer  ◄── SerperDevTool (web search)
                └── Writes complete Pygame script from the GDD
                        │
                [Agent 3] QA Engineer & Code Reviewer
                        └── Reviews, fixes, and outputs final polished code
                                │
                        game.py  ──► python game.py  ──► playable game!
```

---

## Agents

| Agent | Role | Tools |
|---|---|---|
| **Creative Game Designer** | Expands the idea into a structured GDD (title, genre, objective, controls, entities, mechanics) | — |
| **Senior Python Game Developer** | Writes a complete, runnable Pygame script with game loop, events, drawing | SerperDevTool |
| **QA Engineer & Code Reviewer** | Checks for bugs, verifies GDD coverage, improves code quality | — |

## Tasks (Sequential)

| # | Task | Input | Output |
|---|---|---|---|
| 1 | `task_design` | `{game_idea}` from user | Markdown Game Design Document |
| 2 | `task_code` | GDD from task 1 | Complete Pygame Python script |
| 3 | `task_review` | GDD + code from tasks 1–2 | Final polished script + play instructions |

---

## Project Structure

```
game_dev_crew/
├── main.py                       # Entry point — accepts --idea and --output flags
├── requirements.txt
├── .env.example
└── src/game_dev_crew/
    ├── config.py                 # All settings via environment variables
    ├── agents.py                 # build_agents() → (game_designer, senior_engineer, qa_engineer)
    ├── tasks.py                  # build_tasks() → (task_design, task_code, task_review)
    └── crew.py                   # build_crew() assembles the Crew; run_crew() kicks it off and saves game.py
```

---

## Setup

```bash
# 1. Clone the project
git clone https://github.com/abhaykshinil-cyber/game-dev-crew.git
cd game-dev-crew

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API keys
```

---

## Required API Keys

| Variable | Description | Get it from |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini LLM (powers all 3 agents) | https://aistudio.google.com/app/apikey |
| `SERPER_API_KEY` | Web search (used by the developer agent) | https://serper.dev |

---

## Usage

```bash
# Use the default endless runner idea
python main.py

# Supply your own idea
python main.py --idea "A space shooter where you dodge asteroids"

# Custom output filename
python main.py --idea "Snake game with power-ups" --output snake.py

# Suppress verbose agent output
python main.py --quiet --idea "Pong game"
```

### Running the generated game

```bash
pip install pygame
python game.py
```

---

## Sample Output

Running `python main.py --idea "A space shooter where you dodge asteroids"` produces a `game.py` with:

```
## Game Design Document
- Title: Asteroid Dodge
- Genre: Space Shooter / Survival
- Objective: Survive as long as possible by dodging incoming asteroids
- Controls: LEFT/RIGHT arrow keys to move the spaceship
- Entities: Player ship, asteroids (varying sizes), score counter
- Mechanics: Asteroids spawn at the top and fall; game ends on collision
```

...followed by a complete Pygame script that is written to `game.py` and ready to run.

---

## Limitations

- The QA agent performs a **mental review** — it does not execute the code. Rarely, minor runtime bugs may remain.
- Very complex ideas (multiplayer, physics engines, etc.) are out of scope for a single-file Pygame script.
- Generation time depends on the LLM response speed (~1–3 minutes for the full crew run).
- Gemini API free tier has per-minute rate limits which may occasionally cause retries.
