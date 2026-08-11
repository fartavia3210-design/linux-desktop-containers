#!/usr/bin/env bash

unset DBUS_SESSION_BUS_ADDRESS
unset SESSION_MANAGER

export XDG_RUNTIME_DIR=/run/user/$(id -u)
export XDG_SESSION_TYPE=x11
export XDG_CURRENT_DESKTOP=XFCE
export DESKTOP_SESSION=xfce

exec /usr/bin/dbus-run-session -- /usr/local/bin/start-xfce-xrdp
