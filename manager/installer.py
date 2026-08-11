from __future__ import annotations

from pathlib import Path

from manager.catalog import (
    get_desktop,
    get_display_name,
    is_available,
)
from manager.containers import (
    container_exists,
    container_running,
    create_container,
    remove_container,
    start_container,
)
from manager.dependencies import (
    check_dependencies,
    missing_dependencies,
)
from manager.images import (
    ensure_image,
    get_image_id,
    image_exists,
    remove_image,
    update_image,
)
from manager.shortcuts import (
    create_shortcut,
    remove_shortcut,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


class InstallationError(Exception):
    pass


def get_installation_status(
    distro_key: str,
    desktop_key: str
) -> str:
    """
    Estados posibles:

    unavailable
    not-installed
    image-only
    installed
    """

    if not is_available(
        distro_key,
        desktop_key
    ):
        return "unavailable"

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    image = desktop["image"]["remote"]
    container = desktop["container"]["name"]

    if container_exists(container):
        return "installed"

    if image_exists(image):
        return "image-only"

    return "not-installed"


def validate_installation_requirements() -> None:
    """
    Comprueba dependencias y Docker.
    """

    missing = missing_dependencies()

    if missing:
        raise InstallationError(
            "Faltan dependencias: "
            + ", ".join(missing)
        )

    status = check_dependencies()

    if not status["docker"]["running"]:
        raise InstallationError(
            "Docker está instalado, "
            "pero no está funcionando."
        )


def resolve_seccomp(
    desktop: dict
) -> Path | None:
    """
    Resuelve el perfil seccomp definido
    en catalog.json.
    """

    security = desktop.get(
        "security",
        {}
    )

    seccomp = security.get("seccomp")

    if not seccomp:
        return None

    path = REPO_ROOT / seccomp

    if not path.is_file():
        raise InstallationError(
            f"No existe el perfil seccomp: {path}"
        )

    return path


def create_desktop_container(
    distro_key: str,
    desktop_key: str
) -> bool:
    """
    Crea el contenedor utilizando
    la configuración de catalog.json.
    """

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    container = desktop["container"]

    return create_container(
    image=desktop["image"]["remote"],
    name=container["name"],
    container_port=container["port"],
    shm_size=container.get(
        "shm_size",
        "1g"
    ),
    seccomp_profile=resolve_seccomp(
        desktop
    ),
    apparmor_profile=desktop.get(
        "security",
        {}
    ).get(
        "apparmor"
    )
)


def create_desktop_shortcut(
    distro_key: str,
    desktop_key: str
):
    """
    Crea el acceso directo de la distro.
    """

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    display_name = get_display_name(
        distro_key,
        desktop_key
    )

    shortcut = desktop.get(
        "shortcut",
        {}
    )

    name = shortcut.get(
        "name",
        display_name
    )

    return create_shortcut(
        distro_key=distro_key,
        desktop_key=desktop_key,
        name=name
    )


def install_desktop(
    distro_key: str,
    desktop_key: str
) -> bool:
    """
    Instala una distro:

    1. descarga imagen;
    2. crea contenedor;
    3. crea acceso directo.
    """

    if not is_available(
        distro_key,
        desktop_key
    ):
        raise InstallationError(
            f"{get_display_name(distro_key, desktop_key)} "
            "todavía no está disponible."
        )

    validate_installation_requirements()

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    display_name = get_display_name(
        distro_key,
        desktop_key
    )

    image = desktop["image"]["remote"]

    print()
    print("=" * 50)
    print(f"Instalando {display_name}")
    print("=" * 50)
    print()

    print("1/3 Descargando imagen...")

    if not ensure_image(image):
        raise InstallationError(
            "No se pudo descargar la imagen Docker."
        )

    print()
    print("2/3 Creando contenedor...")

    if not create_desktop_container(
        distro_key,
        desktop_key
    ):
        raise InstallationError(
            "No se pudo crear el contenedor."
        )

    print()
    print("3/3 Creando acceso directo...")

    create_desktop_shortcut(
        distro_key,
        desktop_key
    )

    print()
    print(
        f"✓ {display_name} instalado correctamente."
    )

    return True


def recreate_desktop(
    distro_key: str,
    desktop_key: str
) -> bool:
    """
    Elimina y vuelve a crear el contenedor.

    Mantiene la imagen instalada.

    NOTA:
    mientras no implementemos persistencia,
    los cambios internos del contenedor se pierden.
    """

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    container_name = desktop[
        "container"
    ]["name"]

    if not image_exists(
        desktop["image"]["remote"]
    ):
        raise InstallationError(
            "La imagen no está instalada."
        )

    was_running = container_running(
        container_name
    )

    if container_exists(container_name):

        if not remove_container(
            container_name,
            force=True
        ):
            raise InstallationError(
                "No se pudo eliminar "
                "el contenedor anterior."
            )

    if not create_desktop_container(
        distro_key,
        desktop_key
    ):
        raise InstallationError(
            "No se pudo recrear el contenedor."
        )

    create_desktop_shortcut(
        distro_key,
        desktop_key
    )

    if was_running:
        if not start_container(container_name):
            raise InstallationError(
                "El contenedor fue recreado, "
                "pero no pudo iniciarse."
            )

    return True


def update_desktop(
    distro_key: str,
    desktop_key: str
) -> dict:
    """
    Busca una imagen más reciente en GHCR.

    Si la imagen cambió y existe un contenedor,
    lo recrea automáticamente.
    """

    validate_installation_requirements()

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    image = desktop["image"]["remote"]
    container_name = desktop[
        "container"
    ]["name"]

    previous_id = get_image_id(image)

    if not update_image(image):
        raise InstallationError(
            "No se pudo actualizar la imagen."
        )

    current_id = get_image_id(image)

    changed = (
        previous_id != current_id
    )

    recreated = False

    if (
        changed
        and container_exists(container_name)
    ):
        recreate_desktop(
            distro_key,
            desktop_key
        )

        recreated = True

    return {
        "changed": changed,
        "recreated": recreated
    }


def uninstall_desktop(
    distro_key: str,
    desktop_key: str,
    remove_image_too: bool = False
) -> bool:
    """
    Desinstala una combinación.

    Siempre:
    - elimina contenedor;
    - elimina acceso directo.

    Opcionalmente:
    - elimina también la imagen Docker.
    """

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    container_name = desktop[
        "container"
    ]["name"]

    image = desktop["image"]["remote"]

    if not remove_container(
        container_name,
        force=True
    ):
        raise InstallationError(
            "No se pudo eliminar el contenedor."
        )

    if not remove_shortcut(
        distro_key,
        desktop_key
    ):
        raise InstallationError(
            "No se pudo eliminar "
            "el acceso directo."
        )

    if remove_image_too:

        if not remove_image(image):
            raise InstallationError(
                "El contenedor fue eliminado, "
                "pero no se pudo borrar la imagen."
            )

    return True
