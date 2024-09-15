import json
import pathlib
from typing import Any

from punchcard.constants import CONFIG_PATH


def get_user_config() -> dict[Any, Any]:
    with open(str(CONFIG_PATH), "r", encoding="utf-8") as config_file:
        return json.load(config_file)  # type: ignore


def set_user_config(config: dict) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as config_file:
        json.dump(config, config_file)


def create_user_config() -> None:
    if not pathlib.Path(CONFIG_PATH).exists():
        with open(
            "punchcard/config/config.json",
            "r",
            encoding="utf-8",
        ) as default_config:
            default_config = json.load(default_config)

        with CONFIG_PATH.open("w", encoding="utf-8") as config_file:
            json.dump(default_config, config_file)


def update_config(key: str, value: int) -> None:
    config = get_user_config()
    config[key] = value
    set_user_config(config)


if __name__ == "__main__":
    create_user_config()
    c = get_user_config()
    print(CONFIG_PATH)
    print(c)
