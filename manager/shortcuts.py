from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from manager.config import SHORTCUTS_DIR, ensure_directories


LAUNCHER = Path.home() / ".local/bin/linux-desktop-launcher"


def get_shortcut_path(
    distro_key: str,
    desktop_key: str
) -> Path:
    """
    Devuelve la ruta del archivo .desktop.
    """

    filename = (
        f"linux-desktop-containers-"
        f"{distro_key}-{desktop_key}.desktop"
    )

    return SHORTCUTS_DIR / filename


def shortcut_exists(
    distro_key: str,
    desktop_key: str
) -> bool:
    """
    Comprueba si el acceso directo existe.
    """

    return get_shortcut_path(
        distro_key,
        desktop_key
    ).is_file()


def refresh_desktop_database() -> None:
    """
    Actualiza la base de datos de aplicaciones
    si update-desktop-database está disponible.
    """

    command = shutil.which(
        "update-desktop-database"
    )

    if command is None:
        return

    subprocess.run(
        [
            command,
            str(SHORTCUTS_DIR)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )


def create_shortcut(
    *,
    distro_key: str,
    desktop_key: str,
    name: str,
    icon: str = "utilities-terminal"
) -> Path:
    """
    Crea un acceso directo Linux .desktop
    para una distro instalada.
    """

    ensure_directories()

    SHORTCUTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    shortcut = get_shortcut_path(
        distro_key,
        desktop_key
    )

    content = f"""[Desktop Entry]
Type=Application
Version=1.0
Name={name}
Comment=Linux desktop running inside Docker
Exec={LAUNCHER} {distro_key} {desktop_key}
Icon={icon}
Terminal=false
Categories=System;Utility;
StartupNotify=true
"""

    shortcut.write_text(
        content,
        encoding="utf-8"
    )

    shortcut.chmod(0o755)

    refresh_desktop_database()

    return shortcut


def remove_shortcut(
    distro_key: str,
    desktop_key: str
) -> bool:
    """
    Elimina un acceso directo existente.
    """

    shortcut = get_shortcut_path(
        distro_key,
        desktop_key
    )

    if not shortcut.exists():
        return True

    try:
        shortcut.unlink()
        refresh_desktop_database()
        return True

    except OSError:
        return False
