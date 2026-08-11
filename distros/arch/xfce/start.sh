#!/usr/bin/env bash

set -e

ARCH_USER="${ARCH_USER:-arch}"
ARCH_UID="$(id -u "$ARCH_USER")"

mkdir -p /run/dbus
mkdir -p "/run/user/$ARCH_UID"
mkdir -p /var/run/xrdp

chown "$ARCH_USER:$ARCH_USER" "/run/user/$ARCH_UID"
chmod 700 "/run/user/$ARCH_UID"

rm -f /run/dbus/pid
rm -f /var/run/xrdp.pid
rm -f /var/run/xrdp-sesman.pid

dbus-daemon --system --fork

xrdp-sesman --nodaemon &
SESMAN_PID=$!

sleep 1

exec xrdp --nodaemon
