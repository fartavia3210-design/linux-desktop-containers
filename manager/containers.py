from __future__ import annotations

import subprocess
from pathlib import Path


def container_exists(name: str) -> bool:
    """
    Comprueba si un contenedor existe, esté iniciado o detenido.
    """

    result = subprocess.run(
        ["docker", "container", "inspect", name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

    return result.returncode == 0


def container_running(name: str) -> bool:
    """
    Comprueba si un contenedor existe y está ejecutándose.
    """

    if not container_exists(name):
        return False

    result = subprocess.run(
        [
            "docker",
            "inspect",
            "-f",
            "{{.State.Running}}",
            name
        ],
        capture_output=True,
        text=True,
        check=False
    )

    return (
        result.returncode == 0
        and result.stdout.strip() == "true"
    )


def start_container(name: str) -> bool:
    """
    Inicia un contenedor existente.
    """

    if not container_exists(name):
        return False

    if container_running(name):
        return True

    result = subprocess.run(
        ["docker", "start", name],
        check=False
    )

    return result.returncode == 0


def stop_container(name: str) -> bool:
    """
    Detiene un contenedor existente.
    """

    if not container_exists(name):
        return True

    if not container_running(name):
        return True

    result = subprocess.run(
        ["docker", "stop", name],
        check=False
    )

    return result.returncode == 0


def remove_container(name: str, force: bool = False) -> bool:
    """
    Elimina un contenedor.
    """

    if not container_exists(name):
        return True

    command = ["docker", "rm"]

    if force:
        command.append("-f")

    command.append(name)

    result = subprocess.run(
        command,
        check=False
    )

    return result.returncode == 0


def create_container(
    *,
    image: str,
    name: str,
    container_port: int,
    shm_size: str = "1g",
    seccomp_profile: Path | None = None,
    environment: dict[str, str] | None = None
) -> bool:
    """
    Crea un contenedor nuevo sin iniciarlo.

    Docker selecciona automáticamente un puerto libre
    del host y lo publica solamente en 127.0.0.1.
    """

    if container_exists(name):
        return True

    command = [
        "docker",
        "create",
        "--name",
        name,
        "--shm-size",
        shm_size,
        "-p",
        f"127.0.0.1::{container_port}"
    ]

    if seccomp_profile is not None:
        command.extend(
            [
                "--security-opt",
                f"seccomp={seccomp_profile}"
            ]
        )

    if environment:
        for key, value in environment.items():
            command.extend(
                [
                    "-e",
                    f"{key}={value}"
                ]
            )

    command.append(image)

    result = subprocess.run(
        command,
        check=False
    )

    return result.returncode == 0


def get_host_port(
    name: str,
    container_port: int
) -> int | None:
    """
    Obtiene el puerto que Docker asignó automáticamente
    en el host para un puerto del contenedor.
    """

    if not container_exists(name):
        return None

    result = subprocess.run(
        [
            "docker",
            "port",
            name,
            f"{container_port}/tcp"
        ],
        capture_output=True,
        text=True,
        check=False
    )

    if result.returncode != 0:
        return None

    output = result.stdout.strip()

    if not output:
        return None

    try:
        return int(output.rsplit(":", 1)[1])
    except (IndexError, ValueError):
        return None


def get_status(name: str) -> str:
    """
    Devuelve un estado sencillo del contenedor.
    """

    if not container_exists(name):
        return "not-installed"

    if container_running(name):
        return "running"

    return "stopped"
