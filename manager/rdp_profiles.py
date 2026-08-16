from __future__ import annotations

from manager.dependencies import detect_host_distro


class RDPProfileError(ValueError):
    """
    Error de configuración de perfiles RDP.
    """


def _validate_arguments(
    arguments: object,
    *,
    context: str
) -> list[str]:
    """
    Valida una lista de argumentos de FreeRDP.
    """

    if not isinstance(arguments, list):
        raise RDPProfileError(
            f"{context} debe contener una lista "
            f"de argumentos."
        )

    result = []

    for argument in arguments:
        if not isinstance(argument, str):
            raise RDPProfileError(
                f"Todos los argumentos de "
                f"{context} deben ser texto."
            )

        result.append(argument)

    return result


def _get_profile_arguments(
    catalog: dict,
    profile_name: str
) -> list[str]:
    """
    Obtiene los argumentos asociados a un perfil RDP.
    """

    profiles = catalog.get(
        "rdp_profiles",
        {}
    )

    if not isinstance(profiles, dict):
        raise RDPProfileError(
            "rdp_profiles debe ser un objeto."
        )

    profile = profiles.get(profile_name)

    if not isinstance(profile, dict):
        raise RDPProfileError(
            f"Perfil RDP desconocido: "
            f"{profile_name}"
        )

    return _validate_arguments(
        profile.get("arguments"),
        context=(
            f"rdp_profiles.{profile_name}.arguments"
        )
    )


def resolve_rdp_profile(
    catalog: dict,
    rdp: dict
) -> tuple[str | None, list[str]]:
    """
    Resuelve el perfil RDP que corresponde al host.

    Orden:

    1. Si existe un override exacto para el ID del host,
       utiliza ese perfil.
    2. Si no existe, utiliza default_profile.
    3. Mientras migramos el catálogo, conserva soporte
       para rdp.arguments como formato anterior.
    """

    default_profile = rdp.get(
        "default_profile"
    )

    # Compatibilidad con la configuración anterior.
    if default_profile is None:
        legacy_arguments = rdp.get(
            "arguments"
        )

        if legacy_arguments is None:
            raise RDPProfileError(
                "La configuración RDP no tiene "
                "default_profile ni arguments."
            )

        return (
            None,
            _validate_arguments(
                legacy_arguments,
                context="rdp.arguments"
            )
        )

    if not isinstance(default_profile, str):
        raise RDPProfileError(
            "rdp.default_profile debe ser texto."
        )

    overrides = rdp.get(
        "host_profile_overrides",
        {}
    )

    if not isinstance(overrides, dict):
        raise RDPProfileError(
            "rdp.host_profile_overrides "
            "debe ser un objeto."
        )

    host = detect_host_distro()
    host_id = host.get(
        "id",
        ""
    )

    profile_name = overrides.get(
        host_id,
        default_profile
    )

    if not isinstance(profile_name, str):
        raise RDPProfileError(
            "El nombre del perfil RDP "
            "debe ser texto."
        )

    arguments = _get_profile_arguments(
        catalog,
        profile_name
    )

    return profile_name, arguments


def resolve_rdp_arguments(
    catalog: dict,
    rdp: dict
) -> list[str]:
    """
    Devuelve únicamente los argumentos FreeRDP finales.
    """

    _, arguments = resolve_rdp_profile(
        catalog,
        rdp
    )

    return arguments
