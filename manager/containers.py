from __future__ import annotations

import subprocess
from pathlib import Path


def apparmor_enabled() -> bool:
    """
    Comprueba si AppArmor está activo
    en el kernel del host.
    """

    path = Path(
        "/sys/module/apparmor/parameters/enabled"
    )

    if not path.is_file():
        return False

    try:
        value = path.read_text(
            encoding="utf-8"
        ).strip()

        return value.upper().startswith("Y")

    except OSError:
        return False


def selinux_enforcing() -> bool:
    """
    Comprueba si SELinux está activo
    y en modo Enforcing en el host.
    """

    path = Path(
        "/sys/fs/selinux/enforce"
    )

    if not path.is_file():
        return False

    try:
        value = path.read_text(
            encoding="utf-8"
        ).strip()

        return value == "1"

    except OSError:
        return False


def _run(
    command: list[str],
    *,
    capture_output: bool = False
) -> subprocess.CompletedProcess:
    """
    Ejecuta un comando del sistema.
    """

    return subprocess.run(
        command,
        text=True,
        capture_output=capture_output,
        check=False
    )


def container_exists(name: str) -> bool:
    """
    Comprueba si un contenedor existe,
    independientemente de si está iniciado.
    """

    result = _run(
        [
            "docker",
            "inspect",
            name
        ],
        capture_output=True
    )

    return result.returncode == 0


def container_running(name: str) -> bool:
    """
    Comprueba si un contenedor está ejecutándose.
    """

    if not container_exists(name):
        return False

    result = _run(
        [
            "docker",
            "inspect",
            "-f",
            "{{.State.Running}}",
            name
        ],
        capture_output=True
    )

    if result.returncode != 0:
        return False

    return result.stdout.strip().lower() == "true"


def start_container(name: str) -> bool:
    """
    Inicia un contenedor existente.
    """

    if not container_exists(name):
        return False

    if container_running(name):
        return True

    result = _run(
        [
            "docker",
            "start",
            name
        ]
    )

    return result.returncode == 0


def stop_container(name: str) -> bool:
    """
    Detiene un contenedor.

    Si no existe o ya está detenido,
    se considera una operación válida.
    """

    if not container_exists(name):
        return True

    if not container_running(name):
        return True

    result = _run(
        [
            "docker",
            "stop",
            name
        ]
    )

    return result.returncode == 0


def remove_container(
    name: str,
    *,
    force: bool = True
) -> bool:
    """
    Elimina un contenedor.

    Si no existe, devuelve True.
    """

    if not container_exists(name):
        return True

    command = [
        "docker",
        "rm"
    ]

    if force:
        command.append("-f")

    command.append(name)

    result = _run(command)

    return result.returncode == 0


def create_container(
    *,
    image: str,
    name: str,
    container_port: int = 3389,
    shm_size: str = "1g",
    seccomp_profile: str | Path | None = None,
    apparmor_profile: str | None = None,
    environment: dict[str, str] | None = None
) -> bool:
    """
    Crea un contenedor Docker.

    El puerto del host se asigna automáticamente
    y únicamente se publica sobre 127.0.0.1.

    security:
        seccomp_profile
            Perfil seccomp personalizado.

        apparmor_profile
            Perfil AppArmor opcional.

        SELinux
            Si el host utiliza SELinux en modo
            Enforcing, se desactiva únicamente
            el etiquetado SELinux del contenedor
            mediante:

                --security-opt label=disable

            Esto no desactiva SELinux globalmente
            en el host.

    environment:
        Variables de entorno adicionales.
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
        f"127.0.0.1::{container_port}",
    ]

    # --------------------------------------------------------
    # Seccomp
    # --------------------------------------------------------

    if seccomp_profile is not None:

        seccomp_path = Path(
            seccomp_profile
        ).expanduser().resolve()

        if not seccomp_path.is_file():
            print(
                "ERROR: No existe el perfil seccomp:"
            )
            print(
                f"  {seccomp_path}"
            )

            return False

        command.extend(
            [
                "--security-opt",
                f"seccomp={seccomp_path}"
            ]
        )

    # --------------------------------------------------------
    # Seguridad del host
    # --------------------------------------------------------
    #
    # SELinux Enforcing:
    #
    #     --security-opt label=disable
    #
    # AppArmor:
    #
    #     --security-opt apparmor=<perfil>
    #
    # Sin SELinux ni AppArmor:
    #
    #     no se añade ninguna opción LSM adicional.
    # --------------------------------------------------------

    if selinux_enforcing():

        command.extend(
            [
                "--security-opt",
                "label=disable"
            ]
        )

    elif apparmor_profile and apparmor_enabled():

        command.extend(
            [
                "--security-opt",
                f"apparmor={apparmor_profile}"
            ]
        )

    # --------------------------------------------------------
    # Variables de entorno
    # --------------------------------------------------------

    if environment:

        for key, value in environment.items():

            command.extend(
                [
                    "-e",
                    f"{key}={value}"
                ]
            )

    command.append(image)

    result = _run(command)

    return result.returncode == 0


def get_host_port(
    name: str,
    container_port: int = 3389
) -> int | None:
    """
    Obtiene el puerto asignado por Docker
    en el host.
    """

    if not container_exists(name):
        return None

    result = _run(
        [
            "docker",
            "port",
            name,
            f"{container_port}/tcp"
        ],
        capture_output=True
    )

    if result.returncode != 0:
        return None

    output = result.stdout.strip()

    if not output:
        return None

    # Ejemplo:
    #
    # 127.0.0.1:32770

    line = output.splitlines()[0]

    try:
        port_text = line.rsplit(
            ":",
            1
        )[1]

        return int(port_text)

    except (
        IndexError,
        ValueError
    ):
        return None


def get_status(name: str) -> str:
    """
    Devuelve un estado sencillo:

        missing
        running
        stopped
    """

    if not container_exists(name):
        return "missing"

    if container_running(name):
        return "running"

    return "stopped"
