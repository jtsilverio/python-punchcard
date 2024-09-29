from pathlib import Path

# DATABASE
DATABASE_NAME: str = "punchcard.db"
DOT_FOLDER: str = ".punchcard"
DATABASE_PATH: Path = Path.home() / DOT_FOLDER / DATABASE_NAME

# DATE AND TIME FORMATS
DATE_FORMAT: str = "%Y-%m-%d"
TIME_FORMAT: str = "%H:%M"

# CONFIG
CONFIG_PATH: Path = Path.home() / DOT_FOLDER / "config.json"
