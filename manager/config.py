from __future__ import annotations

import json
import os
from pathlib import Path


APP_NAME = "linux-desktop-containers"

HOME = Path.home()

CONFIG_HOME = Path(
    os.environ.get(
        "XDG_CONFIG_HOME",
        HOME / ".config"
    )
)

DATA_HOME = Path(
    os.environ.get(
        "XDG_DATA_HOME",
        HOME / ".local/share"
    )
)

STATE_HOME = Path(
    os.environ.get(
        "XDG_STATE_HOME",
        HOME / ".local/state"
    )
)


CONFIG_DIR = CONFIG_HOME / APP_NAME
DATA_DIR = DATA_HOME / APP_NAME
STATE_DIR = STATE_HOME / APP_NAME

CONFIG_FILE = CONFIG_DIR / "config.json"

SHORTCUTS_DIR = DATA_HOME / "applications"
ICONS_DIR = DATA_DIR / "icons"


DEFAULT_CONFIG = {
    "schema_version": 1,
    "preferences": {
        "auto_create_shortcuts": True,
        "auto_start_after_install": True
    }
}


def ensure_directories() -> None:
    """
    Crea las carpetas locales necesarias para el usuario.
    """

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    ICONS_DIR.mkdir(parents=True, exist_ok=True)


def save_config(config: dict) -> None:
    """
    Guarda la configuración local del usuario.
    """

    ensure_directories()

    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            config,
            file,
            indent=2,
            ensure_ascii=False
        )


def load_config() -> dict:
    """
    Carga la configuración existente.

    Si todavía no existe, crea una configuración
    inicial automáticamente.
    """

    ensure_directories()

    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG.copy())

    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError):
        return DEFAULT_CONFIG.copy()


def initialize() -> dict:
    """
    Inicializa el entorno local de Linux Desktop Containers.
    """

    ensure_directories()
    return load_config()
