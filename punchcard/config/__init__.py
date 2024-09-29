from typing import Any, Dict

from punchcard.config.config_manager import (
    create_user_config_file,
    get_user_config,
    set_user_config,
    update_user_config,
)
from punchcard.config.dataclasses import UserConfig

from .constants import (
    CONFIG_PATH,
    DATABASE_NAME,
    DATABASE_PATH,
    DATE_FORMAT,
    DOT_FOLDER,
    TIME_FORMAT,
)

USER_CONFIG: UserConfig = get_user_config()

__all__ = [
    "create_user_config_file",
    "get_user_config",
    "set_user_config",
    "update_user_config",
    "CONFIG_PATH",
    "DATABASE_NAME",
    "DATABASE_PATH",
    "DATE_FORMAT",
    "DOT_FOLDER",
    "TIME_FORMAT",
]
