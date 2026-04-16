"""
main.py — Entry point for the Game Dev Crew.

Usage
-----
    # Use the built-in default idea
    python main.py

    # Supply your own game idea
    python main.py --idea "A space shooter where you dodge asteroids"

    # Specify where to save the generated game script
    python main.py --idea "Snake game" --output snake.py

Environment
-----------
    Copy .env.example → .env and set:
        GEMINI_API_KEY
        SERPER_API_KEY

Expected output
---------------
    The crew will print agent reasoning to stdout while working.
    On completion, a runnable Pygame script is written to --output (default: game.py).
    Play it with:
        pip install pygame
        python game.py
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent / "src"))

from game_dev_crew.config import Config
from game_dev_crew.crew import build_crew, run_crew

DEFAULT_IDEA = "A fun endless runner where a character jumps over obstacles"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Game Dev Crew — AI-powered Pygame game generator"
    )
    parser.add_argument(
        "--idea",
        type=str,
        default=DEFAULT_IDEA,
        help="One-line game concept for the crew to develop.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output filename for the generated Pygame script (default: game.py).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable verbose agent output.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    cfg = Config()
    if args.quiet:
        cfg.verbose = False
    if args.output:
        cfg.output_game_file = args.output

    cfg.validate()

    crew = build_crew(cfg)
    run_crew(crew, game_idea=args.idea, output_file=cfg.output_game_file)


if __name__ == "__main__":
    main()
