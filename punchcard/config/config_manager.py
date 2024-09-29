import json
import pathlib

from punchcard.config.dataclasses import UserConfig

from .constants import CONFIG_PATH


def get_user_config() -> UserConfig:
    with open(str(CONFIG_PATH), "r", encoding="utf-8") as config_file:
        config_json = json.load(config_file)
        return UserConfig.from_dict(config_json)


def set_user_config(config: UserConfig) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as config_file:
        json.dump(config.to_dict(), config_file)


def create_user_config_file() -> None:
    if not pathlib.Path(CONFIG_PATH).exists():
        with open(
            "punchcard/config/config.json",
            "r",
            encoding="utf-8",
        ) as default_config:
            default_config = json.load(default_config)

        with CONFIG_PATH.open("w", encoding="utf-8") as config_file:
            json.dump(default_config, config_file)


def update_user_config(key: str, value: int) -> None:
    config = get_user_config()
    config[key] = value
    set_user_config(config)
