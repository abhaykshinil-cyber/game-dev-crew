"""
agents.py — CrewAI Agent definitions for the Game Dev Crew.

Agents
------
game_designer    — Creative Game Designer
senior_engineer  — Senior Python Game Developer
qa_engineer      — QA Engineer & Code Reviewer
"""

from crewai import Agent, LLM
from crewai_tools import SerperDevTool

from .config import Config


def build_llm(cfg: Config) -> LLM:
    """
    Construct and return the shared CrewAI LLM wrapper.

    Args:
        cfg: Populated Config dataclass.

    Returns:
        CrewAI LLM instance backed by Gemini 2.5 Flash.
    """
    return LLM(model=cfg.llm_model, api_key=cfg.gemini_api_key)


def build_agents(cfg: Config) -> tuple[Agent, Agent, Agent]:
    """
    Instantiate all three crew agents.

    Args:
        cfg: Populated Config dataclass.

    Returns:
        Tuple of (game_designer, senior_engineer, qa_engineer).
    """
    llm = build_llm(cfg)
    search_tool = SerperDevTool(api_key=cfg.serper_api_key)

    game_designer = Agent(
        role="Creative Game Designer",
        goal="Come up with fun, feasible game concepts and detailed mechanics based on the user idea.",
        backstory=(
            "You are an experienced game designer. "
            "You excel at turning vague ideas into clear, exciting game designs including: "
            "core loop, rules, win/lose conditions, basic entities (player, enemies, items), "
            "controls and feel. "
            "Keep it simple enough to implement in pure Python + Pygame in one file."
        ),
        verbose=cfg.verbose,
        llm=llm,
    )

    senior_engineer = Agent(
        role="Senior Python Game Developer",
        goal="Write clean, working Python code (using Pygame) for the described game.",
        backstory=(
            "You are a senior software engineer specialised in Python game development with Pygame. "
            "You write structured, readable code with: "
            "proper game loop, event handling, drawing, "
            "comments explaining key parts, and error handling where needed. "
            "You always produce a complete, runnable .py file."
        ),
        tools=[search_tool],
        verbose=cfg.verbose,
        llm=llm,
    )

    qa_engineer = Agent(
        role="QA Engineer & Code Reviewer",
        goal="Test, review, and improve the code for bugs, playability, and completeness.",
        backstory=(
            "You are a meticulous QA engineer and code reviewer. "
            "You carefully check: does the code run without errors? "
            "Does it implement ALL the designed features? "
            "Is it fun/playable? Any obvious balance issues? "
            "Code style, variable names, comments. "
            "You suggest fixes or small improvements and output the FINAL improved code."
        ),
        verbose=cfg.verbose,
        llm=llm,
    )

    return game_designer, senior_engineer, qa_engineer
