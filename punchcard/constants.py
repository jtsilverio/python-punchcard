from pathlib import Path

DATABASE_NAME = "punchcard.db"
DOT_FOLDER = ".punchcard"
DATABASE_PATH = Path.home() / DOT_FOLDER / DATABASE_NAME
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
CONFIG_PATH = Path.home() / DOT_FOLDER / "config.json"
