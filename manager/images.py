from __future__ import annotations

import subprocess


def image_exists(image: str) -> bool:
    """
    Comprueba si una imagen Docker existe localmente.
    """

    result = subprocess.run(
        [
            "docker",
            "image",
            "inspect",
            image
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )

    return result.returncode == 0


def pull_image(image: str) -> bool:
    """
    Descarga una imagen desde el registry.

    Devuelve True si la descarga fue exitosa.
    """

    print()
    print(f"Descargando imagen:")
    print(f"  {image}")
    print()

    result = subprocess.run(
        [
            "docker",
            "pull",
            image
        ],
        check=False
    )

    return result.returncode == 0


def ensure_image(image: str) -> bool:
    """
    Garantiza que una imagen exista localmente.

    Si ya existe, no vuelve a descargarla.
    Si no existe, intenta descargarla.
    """

    if image_exists(image):
        return True

    return pull_image(image)


def update_image(image: str) -> bool:
    """
    Fuerza una comprobación/actualización de la imagen
    descargándola nuevamente desde el registry.
    """

    return pull_image(image)


def remove_image(image: str) -> bool:
    """
    Elimina una imagen Docker local.
    """

    if not image_exists(image):
        return True

    result = subprocess.run(
        [
            "docker",
            "image",
            "rm",
            image
        ],
        check=False
    )

    return result.returncode == 0


def get_image_id(image: str) -> str | None:
    """
    Devuelve el ID de una imagen Docker local.
    """

    if not image_exists(image):
        return None

    result = subprocess.run(
        [
            "docker",
            "image",
            "inspect",
            image,
            "--format",
            "{{.Id}}"
        ],
        capture_output=True,
        text=True,
        check=False
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip() or None
