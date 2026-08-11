#!/usr/bin/env bash

set -e

APP_NAME="linux-desktop-containers"
DISPLAY_NAME="Linux Desktop Containers"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BIN_DIR="$HOME/.local/bin"
APPLICATIONS_DIR="$HOME/.local/share/applications"

MAIN_COMMAND="$BIN_DIR/linux-desktops"
DESKTOP_LAUNCHER="$BIN_DIR/linux-desktop-launcher"

DESKTOP_FILE="$APPLICATIONS_DIR/linux-desktop-containers.desktop"


print_header() {
    echo
    echo "=========================================="
    echo "       Linux Desktop Containers"
    echo "=========================================="
    echo
}


print_header


# ============================================================
# Python
# ============================================================

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: Python 3 no está instalado."
    echo
    echo "Por ahora Python debe instalarse antes de ejecutar"
    echo "Linux Desktop Containers."
    echo
    exit 1
fi


cd "$REPO_ROOT"


# ============================================================
# Detectar host
# ============================================================

echo "Detectando sistema..."

HOST_INFO="$(
python3 -c '
from manager.dependencies import detect_host_distro
d = detect_host_distro()
print(d["name"])
'
)"

PACKAGE_MANAGER="$(
python3 -c '
from manager.dependencies import detect_package_manager
print(detect_package_manager() or "")
'
)"

echo
echo "Sistema: $HOST_INFO"

if [ -n "$PACKAGE_MANAGER" ]; then
    echo "Gestor de paquetes: $PACKAGE_MANAGER"
else
    echo "Gestor de paquetes: no soportado"
fi

echo


# ============================================================
# Dependencias
# ============================================================

MISSING_COUNT="$(
python3 -c '
from manager.dependencies import missing_dependencies
print(len(missing_dependencies()))
'
)"

if [ "$MISSING_COUNT" -gt 0 ]; then

    echo "Se encontraron dependencias faltantes:"
    echo

    python3 -c '
from manager.dependencies import missing_dependencies

for dependency in missing_dependencies():
    print(f"  - {dependency}")
'

    echo

    if [ "$PACKAGE_MANAGER" = "pacman" ] || \
   [ "$PACKAGE_MANAGER" = "apt" ] || \
   [ "$PACKAGE_MANAGER" = "dnf" ]; then

        read -r -p "¿Instalar automáticamente? [S/n]: " ANSWER

        ANSWER="${ANSWER:-S}"

        case "$ANSWER" in
            s|S|si|SI|sí|Sí|y|Y|yes|YES)

                echo
                echo "Instalando dependencias..."
                echo

                if ! python3 -c '
from manager.dependencies import install_missing_dependencies
raise SystemExit(0 if install_missing_dependencies() else 1)
'
                then
                    echo
                    echo "ERROR: No fue posible instalar todas las dependencias."
                    exit 1
                fi

                ;;

            *)
                echo
                echo "Instalación cancelada."
                echo
                echo "Instala las dependencias faltantes y vuelve a ejecutar:"
                echo
                echo "  ./install.sh"
                echo
                exit 1
                ;;
        esac

    else

        echo "La instalación automática todavía no está"
        echo "implementada para este sistema."
        echo
        echo "Instala las dependencias manualmente y vuelve"
        echo "a ejecutar ./install.sh."
        echo

        exit 1
    fi

else

    echo "Dependencias principales: ✅ completas"
    echo
fi


# ============================================================
# Docker
# ============================================================

DOCKER_RUNNING="$(
python3 -c '
from manager.dependencies import docker_running
print("yes" if docker_running() else "no")
'
)"

if [ "$DOCKER_RUNNING" != "yes" ]; then

    echo "Docker está instalado pero no responde."
    echo
    echo "Intentando iniciar docker.service..."
    echo

    if python3 -c '
from manager.dependencies import start_docker_service
raise SystemExit(0 if start_docker_service() else 1)
'
    then
        echo "Docker: ✅ activo"
    else
        echo
        echo "No fue posible utilizar Docker."
        echo
        echo "Puede deberse a:"
        echo "  - docker.service detenido"
        echo "  - permisos insuficientes"
        echo "  - configuración del daemon"
        echo
        echo "Linux Desktop Containers necesita que:"
        echo
        echo "  docker info"
        echo
        echo "funcione con tu usuario."
        echo
        exit 1
    fi
fi


# ============================================================
# Directorios
# ============================================================

echo
echo "Creando directorios..."

mkdir -p "$BIN_DIR"
mkdir -p "$APPLICATIONS_DIR"


# ============================================================
# Comandos globales
# ============================================================

echo "Instalando comando linux-desktops..."

ln -sfn \
    "$REPO_ROOT/linux-desktops" \
    "$MAIN_COMMAND"


echo "Instalando launcher de escritorios..."

ln -sfn \
    "$REPO_ROOT/launchers/desktop-launcher" \
    "$DESKTOP_LAUNCHER"


chmod +x "$REPO_ROOT/linux-desktops"
chmod +x "$REPO_ROOT/launchers/desktop-launcher"


# ============================================================
# Acceso directo del administrador
# ============================================================

echo "Creando acceso directo..."

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=$DISPLAY_NAME
Comment=Manage Linux desktop containers
Exec=$MAIN_COMMAND
Icon=utilities-terminal
Terminal=true
Categories=System;Utility;
StartupNotify=true
EOF

chmod +x "$DESKTOP_FILE"


# ============================================================
# Actualizar menú de aplicaciones
# ============================================================

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$APPLICATIONS_DIR" >/dev/null 2>&1 || true
fi


# ============================================================
# Configuración local
# ============================================================

echo "Inicializando configuración..."

python3 -c '
from manager.config import initialize
initialize()
'


# ============================================================
# Resumen final
# ============================================================

echo
echo "Comprobando instalación..."
echo

python3 - <<'PY'
from manager.dependencies import check_dependencies

status = check_dependencies()

print(
    f"Python         ✅ {status['python']['version']}"
)

print(
    f"Docker         "
    f"{'✅ activo' if status['docker']['running'] else '❌'}"
)

print(
    f"Docker Buildx  "
    f"{'✅' if status['docker_buildx']['installed'] else '❌'}"
)

print(
    f"Git            "
    f"{'✅' if status['git']['installed'] else '❌'}"
)

print(
    f"Bash           "
    f"{'✅' if status['bash']['installed'] else '❌'}"
)

print(
    f"FreeRDP        "
    f"{'✅' if status['freerdp']['installed'] else '❌'} "
    f"{status['freerdp']['client'] or ''}"
)
PY


echo
echo "=========================================="
echo "       Instalación completada"
echo "=========================================="
echo
echo "Puedes ejecutar:"
echo
echo "  linux-desktops"
echo
echo "o buscar:"
echo
echo "  Linux Desktop Containers"
echo
echo "en tu menú de aplicaciones."
echo
