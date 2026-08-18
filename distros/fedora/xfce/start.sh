#!/usr/bin/env bash

set -euo pipefail

RDP_USER="${RDP_USER:-fedora}"

# ============================================================
# Limpiar PID antiguos
# ============================================================

rm -f \
    /run/xrdp/xrdp.pid \
    /run/xrdp/xrdp-sesman.pid \
    /run/dbus/pid

# ============================================================
# D-Bus del sistema
# ============================================================

mkdir -p /run/dbus

dbus-daemon \
    --system \
    --fork

# ============================================================
# Runtime XRDP
# ============================================================

mkdir -p /run/xrdp

chown xrdp:xrdp /run/xrdp
chmod 755 /run/xrdp

# ============================================================
# Socket X11
# ============================================================

mkdir -p /tmp/.X11-unix
chmod 1777 /tmp/.X11-unix

# ============================================================
# Runtime del usuario Fedora
# ============================================================

RDP_UID="$(id -u "$RDP_USER")"
RDP_GID="$(id -g "$RDP_USER")"

mkdir -p "/run/user/${RDP_UID}"

chown \
    "${RDP_UID}:${RDP_GID}" \
    "/run/user/${RDP_UID}"

chmod 700 "/run/user/${RDP_UID}"

# ============================================================
# XRDP
# ============================================================

/usr/sbin/xrdp-sesman --nodaemon &

exec /usr/sbin/xrdp --nodaemon
