"""
tasks.py — CrewAI Task definitions for the Game Dev Crew.

Tasks (executed sequentially)
------------------------------
task_design  — Produce a Game Design Document from the user's idea.
task_code    — Write a complete Pygame script from the GDD.
task_review  — Review, fix, and finalise the Pygame script.
"""

from crewai import Task, Agent


def build_tasks(
    game_designer: Agent,
    senior_engineer: Agent,
    qa_engineer: Agent,
) -> tuple[Task, Task, Task]:
    """
    Create and return the three sequential tasks.

    The context chain ensures that each downstream task receives the full
    output of all upstream tasks:
      task_code   receives → task_design
      task_review receives → task_design + task_code

    Args:
        game_designer:   Agent assigned to design the game.
        senior_engineer: Agent assigned to write the code.
        qa_engineer:     Agent assigned to review the code.

    Returns:
        Tuple of (task_design, task_code, task_review).
    """

    task_design = Task(
        description=(
            "Take the user's game idea: {game_idea}\n"
            "1. Clarify and expand it into a fun, simple 2D game.\n"
            "2. Describe: objective, controls, entities, win/lose conditions.\n"
            "3. Keep scope small (one level, basic mechanics).\n\n"
            "Output format:\n"
            "## Game Design Document\n"
            "- Title: ...\n"
            "- Genre: ...\n"
            "- Objective: ...\n"
            "- Controls: ...\n"
            "- Entities: ...\n"
            "- Mechanics: ..."
        ),
        expected_output="A clear markdown Game Design Document",
        agent=game_designer,
    )

    task_code = Task(
        description=(
            "Using the game design from the previous task, "
            "write a COMPLETE, standalone Python script using Pygame that implements the game.\n"
            "- Include: import pygame, sys, random (if needed)\n"
            "- Full game loop: init, events, update, draw\n"
            "- Make it runnable with: python game.py\n"
            "- Add simple inline comments\n"
            "- The main game loop MUST be at the top-level scope, not inside a function\n"
            "- Final answer MUST contain ONLY the Python code and brief play instructions"
        ),
        expected_output="A complete, runnable Pygame Python script",
        agent=senior_engineer,
        context=[task_design],
    )

    task_review = Task(
        description=(
            "Review the Python code from the previous task.\n"
            "1. Check for syntax / runtime errors.\n"
            "2. Verify it matches the Game Design Document.\n"
            "3. Confirm it has: pygame.init(), event loop, quit handling, drawing.\n"
            "4. Suggest and apply fixes / improvements as needed.\n"
            "5. Output the FINAL, improved, ready-to-run code.\n\n"
            "Your final answer MUST contain ONLY the complete Python code along "
            "with the instructions on how to play the game."
        ),
        expected_output="Final polished, runnable Pygame Python script with play instructions",
        agent=qa_engineer,
        context=[task_design, task_code],
    )

    return task_design, task_code, task_review
