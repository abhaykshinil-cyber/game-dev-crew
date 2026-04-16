"""
config.py — Centralised configuration for the Game Dev Crew.
"""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    # ── LLM ──────────────────────────────────────────────────────────────────
    gemini_api_key: str = field(
        default_factory=lambda: os.environ.get("GEMINI_API_KEY", "")
    )
    llm_model: str = field(
        default_factory=lambda: os.environ.get("LLM_MODEL", "gemini/gemini-2.5-flash")
    )

    # ── Serper (web search for the developer agent) ───────────────────────────
    serper_api_key: str = field(
        default_factory=lambda: os.environ.get("SERPER_API_KEY", "")
    )

    # ── Output ────────────────────────────────────────────────────────────────
    # File where the final Pygame script is written
    output_game_file: str = field(
        default_factory=lambda: os.environ.get("OUTPUT_GAME_FILE", "game.py")
    )

    # ── CrewAI verbosity ──────────────────────────────────────────────────────
    verbose: bool = True

    def validate(self) -> None:
        """Raise ValueError for any required-but-missing keys."""
        missing = []
        if not self.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        if not self.serper_api_key:
            missing.append("SERPER_API_KEY")
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                "Copy .env.example → .env and fill in the values."
            )
