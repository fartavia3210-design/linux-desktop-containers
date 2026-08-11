from __future__ import annotations

import os
import platform
import shutil
import subprocess
from pathlib import Path


# ============================================================
# Utilidades generales
# ============================================================

def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def run_command(
    command: list[str],
    *,
    quiet: bool = False
) -> bool:

    try:
        result = subprocess.run(
            command,
            stdout=(
                subprocess.DEVNULL
                if quiet
                else None
            ),
            stderr=(
                subprocess.DEVNULL
                if quiet
                else None
            ),
            check=False
        )

        return result.returncode == 0

    except (OSError, FileNotFoundError):
        return False


# ============================================================
# Docker
# ============================================================

def docker_running() -> bool:
    if not command_exists("docker"):
        return False

    return run_command(
        ["docker", "info"],
        quiet=True
    )


def docker_buildx_available() -> bool:
    if not command_exists("docker"):
        return False

    return run_command(
        [
            "docker",
            "buildx",
            "version"
        ],
        quiet=True
    )


# ============================================================
# FreeRDP
# ============================================================

def detect_freerdp() -> str | None:
    """
    Busca clientes FreeRDP conocidos.

    Debian 13:
        xfreerdp3

    Arch:
        xfreerdp3

    Fedora:
        xfreerdp

    También contempla los clientes SDL.
    """

    candidates = [
        "xfreerdp3",
        "sdl-freerdp3",
        "xfreerdp",
        "sdl-freerdp",
    ]

    for command in candidates:
        path = shutil.which(command)

        if path:
            return command

    return None


# ============================================================
# Detección de distribución
# ============================================================

def detect_host_distro() -> dict:
    """
    Lee /etc/os-release.

    Retorna por ejemplo:

    {
        "id": "cachyos",
        "id_like": ["arch"],
        "name": "CachyOS"
    }
    """

    os_release = Path(
        "/etc/os-release"
    )

    data = {}

    if os_release.is_file():

        for raw_line in os_release.read_text(
            encoding="utf-8",
            errors="ignore"
        ).splitlines():

            line = raw_line.strip()

            if (
                not line
                or line.startswith("#")
                or "=" not in line
            ):
                continue

            key, value = line.split(
                "=",
                1
            )

            value = value.strip().strip(
                "\"'"
            )

            data[key] = value

    distro_id = data.get(
        "ID",
        ""
    ).lower()

    id_like = data.get(
        "ID_LIKE",
        ""
    ).lower().split()

    name = data.get(
        "PRETTY_NAME",
        data.get(
            "NAME",
            distro_id or "Linux"
        )
    )

    return {
        "id": distro_id,
        "id_like": id_like,
        "name": name
    }


def detect_package_manager() -> str | None:
    """
    Retorna:

        pacman
        apt
        dnf
        None
    """

    distro = detect_host_distro()

    distro_id = distro["id"]
    id_like = distro["id_like"]

    # Arch y derivados
    if (
        distro_id in {
            "arch",
            "cachyos",
            "manjaro"
        }
        or "arch" in id_like
    ):
        if command_exists("pacman"):
            return "pacman"

    # Debian, Ubuntu y derivados
    if (
        distro_id in {
            "debian",
            "ubuntu",
            "xubuntu",
            "lubuntu",
            "linuxmint",
            "pop"
        }
        or "debian" in id_like
        or "ubuntu" in id_like
    ):
        if (
            command_exists("apt")
            or command_exists("apt-get")
        ):
            return "apt"

    # Fedora y derivados
    if (
        distro_id in {
            "fedora"
        }
        or "fedora" in id_like
        or "rhel" in id_like
    ):
        if command_exists("dnf"):
            return "dnf"

    # Fallback por comandos disponibles
    if command_exists("pacman"):
        return "pacman"

    if (
        command_exists("apt")
        or command_exists("apt-get")
    ):
        return "apt"

    if command_exists("dnf"):
        return "dnf"

    return None


# ============================================================
# Estado de dependencias
# ============================================================

def check_dependencies() -> dict:
    freerdp_client = detect_freerdp()

    docker_installed = command_exists(
        "docker"
    )

    return {
        "python": {
            "installed": True,
            "version": platform.python_version()
        },

        "docker": {
            "installed": docker_installed,
            "running": (
                docker_running()
                if docker_installed
                else False
            )
        },

        "docker_buildx": {
            "installed": (
                docker_buildx_available()
                if docker_installed
                else False
            )
        },

        "git": {
            "installed": command_exists(
                "git"
            )
        },

        "bash": {
            "installed": command_exists(
                "bash"
            )
        },

        "freerdp": {
            "installed": (
                freerdp_client is not None
            ),
            "client": freerdp_client
        }
    }


def missing_dependencies() -> list[str]:
    status = check_dependencies()

    missing = []

    for dependency in [
        "python",
        "docker",
        "docker_buildx",
        "git",
        "bash",
        "freerdp",
    ]:

        if not status[
            dependency
        ]["installed"]:

            missing.append(
                dependency
            )

    return missing


# ============================================================
# Mapeo dependencia -> paquete
# ============================================================

PACKAGE_MAP = {

    # --------------------------------------------------------
    # Arch Linux / CachyOS / Manjaro
    # --------------------------------------------------------

    "pacman": {
        "python": "python",
        "docker": "docker",
        "docker_buildx": "docker-buildx",
        "git": "git",
        "bash": "bash",
        "freerdp": "freerdp",
    },

    # --------------------------------------------------------
    # Debian / Ubuntu
    # --------------------------------------------------------

    "apt": {
        "python": "python3",
        "docker": "docker.io",
        "docker_buildx": "docker-buildx",
        "git": "git",
        "bash": "bash",
        "freerdp": "freerdp3-x11",
    },

    # --------------------------------------------------------
    # Fedora
    # --------------------------------------------------------

    "dnf": {
        "python": "python3",
        "docker": "moby-engine",
        "docker_buildx": "docker-buildx",
        "git": "git",
        "bash": "bash",
        "freerdp": "freerdp",
    },
}


def get_installation_plan() -> dict:
    manager = detect_package_manager()

    missing = missing_dependencies()

    if not manager:
        return {
            "manager": None,
            "missing": missing,
            "packages": []
        }

    mapping = PACKAGE_MAP.get(
        manager,
        {}
    )

    packages = []

    for dependency in missing:

        package = mapping.get(
            dependency
        )

        if (
            package
            and package not in packages
        ):
            packages.append(
                package
            )

    return {
        "manager": manager,
        "missing": missing,
        "packages": packages
    }


# ============================================================
# Instalación automática
# ============================================================

def install_missing_dependencies() -> bool:
    plan = get_installation_plan()

    manager = plan[
        "manager"
    ]

    packages = plan[
        "packages"
    ]

    missing = plan[
        "missing"
    ]

    if not missing:
        return True

    if not manager:
        print(
            "ERROR: No se pudo detectar "
            "un gestor de paquetes compatible."
        )
        return False

    if not packages:
        print(
            "ERROR: No existe un plan de "
            "instalación para las dependencias "
            "faltantes."
        )
        return False

    print()
    print(
        "Paquetes que se instalarán:"
    )

    for package in packages:
        print(
            f"  - {package}"
        )

    print()

    # --------------------------------------------------------
    # pacman
    # --------------------------------------------------------

    if manager == "pacman":

        return run_command(
            [
                "sudo",
                "pacman",
                "-S",
                "--needed",
                "--noconfirm",
                *packages
            ]
        )

    # --------------------------------------------------------
    # apt
    # --------------------------------------------------------

    if manager == "apt":

        apt_command = (
            "apt-get"
            if command_exists("apt-get")
            else "apt"
        )

        print(
            "Actualizando índices de APT..."
        )

        if not run_command(
            [
                "sudo",
                apt_command,
                "update"
            ]
        ):
            return False

        print()
        print(
            "Instalando dependencias..."
        )

        return run_command(
            [
                "sudo",
                apt_command,
                "install",
                "-y",
                *packages
            ]
        )

    # --------------------------------------------------------
    # dnf
    # --------------------------------------------------------

    if manager == "dnf":

        return run_command(
            [
                "sudo",
                "dnf",
                "install",
                "-y",
                *packages
            ]
        )

    return False


# ============================================================
# Servicio Docker
# ============================================================

def start_docker_service() -> bool:
    """
    Inicia Docker y lo habilita para
    futuros arranques.
    """

    if not command_exists(
        "systemctl"
    ):
        return False

    return run_command(
        [
            "sudo",
            "systemctl",
            "enable",
            "--now",
            "docker.service"
        ]
    )
