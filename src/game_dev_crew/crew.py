"""
crew.py — Crew assembly and execution.

Assembles the three agents and three tasks into a CrewAI Crew and
provides a helper that kicks it off and writes the final Pygame script
to disk.
"""

import re
from pathlib import Path

from crewai import Crew, Process

from .config import Config
from .agents import build_agents
from .tasks import build_tasks


def build_crew(cfg: Config) -> Crew:
    """
    Assemble and return the game-development Crew.

    Args:
        cfg: Populated Config dataclass.

    Returns:
        Crew instance configured for sequential process execution.
    """
    game_designer, senior_engineer, qa_engineer = build_agents(cfg)
    task_design, task_code, task_review = build_tasks(
        game_designer, senior_engineer, qa_engineer
    )

    return Crew(
        agents=[game_designer, senior_engineer, qa_engineer],
        tasks=[task_design, task_code, task_review],
        process=Process.sequential,
        verbose=cfg.verbose,
    )


def run_crew(crew: Crew, game_idea: str, output_file: str) -> str:
    """
    Kick off the crew for a given game idea and save the result.

    The function extracts the Python code block from the final agent output
    and writes it to *output_file*.  If no fenced code block is found, the
    raw output is saved as-is.

    Args:
        crew:        Assembled Crew instance.
        game_idea:   One-line game concept supplied by the user.
        output_file: Path where the final game.py will be written.

    Returns:
        The final raw output string from the crew.
    """
    print(f"\n[Crew] Starting with idea: '{game_idea}'")
    result = crew.kickoff(inputs={"game_idea": game_idea})
    raw = str(result)

    # Extract Python code from fenced block, if present
    code_match = re.search(r"```(?:python)?\s*\n(.*?)```", raw, re.DOTALL)
    code = code_match.group(1).strip() if code_match else raw.strip()

    Path(output_file).write_text(code, encoding="utf-8")
    print(f"\n[Crew] Game script saved to: {output_file}")
    print("[Crew] Run it with: python " + output_file)

    return raw
