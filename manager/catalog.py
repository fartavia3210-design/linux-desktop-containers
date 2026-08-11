from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_FILE = REPO_ROOT / "catalog.json"


class CatalogError(Exception):
    pass


def load_catalog() -> dict:
    """
    Carga y valida el catálogo principal.
    """

    try:
        with CATALOG_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:
            catalog = json.load(file)

    except FileNotFoundError as exc:
        raise CatalogError(
            f"No existe catalog.json en {CATALOG_FILE}"
        ) from exc

    except json.JSONDecodeError as exc:
        raise CatalogError(
            f"catalog.json no es válido: {exc}"
        ) from exc

    if "distros" not in catalog:
        raise CatalogError(
            "catalog.json no contiene la sección 'distros'."
        )

    return catalog


def get_distros() -> dict:
    """
    Devuelve todas las distribuciones.
    """

    return load_catalog()["distros"]


def get_distro(distro_key: str) -> dict:
    """
    Obtiene una distribución por su identificador.
    """

    distros = get_distros()

    if distro_key not in distros:
        raise CatalogError(
            f"Distribución desconocida: {distro_key}"
        )

    return distros[distro_key]


def get_desktop(
    distro_key: str,
    desktop_key: str
) -> dict:
    """
    Obtiene una combinación distro + escritorio.
    """

    distro = get_distro(distro_key)

    desktops = distro.get("desktops", {})

    if desktop_key not in desktops:
        raise CatalogError(
            f"Escritorio desconocido: "
            f"{distro_key}/{desktop_key}"
        )

    return desktops[desktop_key]


def is_available(
    distro_key: str,
    desktop_key: str
) -> bool:
    """
    Indica si la combinación está publicada.
    """

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    return desktop.get(
        "available",
        False
    )


def get_display_name(
    distro_key: str,
    desktop_key: str
) -> str:
    """
    Devuelve un nombre como:
    Arch Linux + XFCE
    """

    distro = get_distro(distro_key)

    desktop = get_desktop(
        distro_key,
        desktop_key
    )

    return (
        f"{distro['name']} + "
        f"{desktop['name']}"
    )
