from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def command_exists(command: str) -> bool:
    """
    Comprueba si un comando existe en el PATH.
    """

    return shutil.which(command) is not None


def docker_running() -> bool:
    """
    Comprueba si Docker responde correctamente.
    """

    if not command_exists("docker"):
        return False

    result = subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

    return result.returncode == 0


def detect_freerdp() -> str | None:
    """
    Detecta un cliente FreeRDP compatible.
    """

    clients = [
        "xfreerdp3",
        "sdl-freerdp3",
        "xfreerdp"
    ]

    for client in clients:
        if command_exists(client):
            return client

    return None


def detect_host_distro() -> dict:
    """
    Detecta la distribución Linux del host
    usando /etc/os-release.
    """

    os_release = Path("/etc/os-release")

    if not os_release.is_file():
        return {
            "id": None,
            "id_like": [],
            "name": "Unknown Linux"
        }

    data = {}

    for line in os_release.read_text(
        encoding="utf-8"
    ).splitlines():

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        data[key] = value.strip().strip('"')

    distro_id = data.get("ID")

    id_like = data.get(
        "ID_LIKE",
        ""
    ).split()

    return {
        "id": distro_id,
        "id_like": id_like,
        "name": data.get(
            "PRETTY_NAME",
            distro_id or "Unknown Linux"
        )
    }


def detect_package_manager() -> str | None:
    """
    Detecta el gestor de paquetes principal.
    """

    distro = detect_host_distro()

    distro_id = distro["id"]
    id_like = distro["id_like"]

    if (
        distro_id in {"arch", "cachyos", "manjaro"}
        or "arch" in id_like
    ):
        return "pacman"

    if (
        distro_id in {"debian", "ubuntu"}
        or "debian" in id_like
        or "ubuntu" in id_like
    ):
        return "apt"

    if (
        distro_id == "fedora"
        or "fedora" in id_like
        or "rhel" in id_like
    ):
        return "dnf"

    return None


def check_dependencies() -> dict:
    """
    Devuelve el estado de las dependencias principales.
    """

    freerdp = detect_freerdp()

    return {
        "python": {
            "installed": True,
            "version": (
                f"{sys.version_info.major}."
                f"{sys.version_info.minor}."
                f"{sys.version_info.micro}"
            )
        },

        "docker": {
            "installed": command_exists("docker"),
            "running": docker_running()
        },

        "git": {
            "installed": command_exists("git")
        },

        "bash": {
            "installed": command_exists("bash")
        },

        "freerdp": {
            "installed": freerdp is not None,
            "client": freerdp
        },

        "docker_buildx": {
            "installed": (
                subprocess.run(
                    ["docker", "buildx", "version"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False
                ).returncode == 0
                if command_exists("docker")
                else False
            )
        }
    }


def missing_dependencies() -> list[str]:
    """
    Devuelve las dependencias faltantes.
    """

    status = check_dependencies()

    missing = []

    if not status["docker"]["installed"]:
        missing.append("docker")

    if not status["docker_buildx"]["installed"]:
        missing.append("docker_buildx")

    if not status["git"]["installed"]:
        missing.append("git")

    if not status["bash"]["installed"]:
        missing.append("bash")

    if not status["freerdp"]["installed"]:
        missing.append("freerdp")

    return missing


def get_installation_plan() -> dict:
    """
    Devuelve qué paquetes habría que instalar
    según el gestor de paquetes detectado.

    Por ahora la instalación automática está
    implementada únicamente para Arch/CachyOS.
    """

    manager = detect_package_manager()

    missing = missing_dependencies()

    packages = []

    if manager == "pacman":

        package_map = {
            "docker": "docker",
            "docker_buildx": "docker-buildx",
            "git": "git",
            "bash": "bash",
            "freerdp": "freerdp"
        }

        for dependency in missing:
            package = package_map.get(dependency)

            if package and package not in packages:
                packages.append(package)

    return {
        "manager": manager,
        "missing": missing,
        "packages": packages
    }


def install_missing_dependencies() -> bool:
    """
    Instala automáticamente las dependencias
    faltantes.

    Actualmente soportado:
    - Arch Linux
    - CachyOS
    - Manjaro
    - otros sistemas ID_LIKE=arch
    """

    plan = get_installation_plan()

    manager = plan["manager"]
    packages = plan["packages"]
    missing = plan["missing"]

    if not missing:
        return True

    if manager != "pacman":
        print(
            "La instalación automática todavía "
            "no está disponible para este sistema."
        )

        return False

    if not packages:
        return True

    print()
    print("Paquetes que se instalarán:")
    print()

    for package in packages:
        print(f"  - {package}")

    print()

    command = [
        "sudo",
        "pacman",
        "-S",
        "--needed",
        "--noconfirm",
        *packages
    ]

    result = subprocess.run(
        command,
        check=False
    )

    return result.returncode == 0


def start_docker_service() -> bool:
    """
    Intenta habilitar e iniciar Docker mediante systemd.
    """

    if not command_exists("docker"):
        return False

    if docker_running():
        return True

    if not command_exists("systemctl"):
        return False

    result = subprocess.run(
        [
            "sudo",
            "systemctl",
            "enable",
            "--now",
            "docker.service"
        ],
        check=False
    )

    if result.returncode != 0:
        return False

    return docker_running()
