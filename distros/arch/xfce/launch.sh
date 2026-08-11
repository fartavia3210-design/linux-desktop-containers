#!/usr/bin/env bash

set -e

IMAGE="arch-xfce:1.0.0"
CONTAINER="arch-xfce"
HOST_PORT="3389"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

SECCOMP_PROFILE="$REPO_ROOT/common/security/seccomp-brave.json"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "No existe la imagen $IMAGE"
    exit 1
fi

if docker container inspect "$CONTAINER" >/dev/null 2>&1; then
    if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER")" != "true" ]; then
        echo "Iniciando contenedor $CONTAINER..."
        docker start "$CONTAINER" >/dev/null
    fi
else
    echo "Creando contenedor $CONTAINER..."

    docker run -d \
        --name "$CONTAINER" \
        --security-opt "seccomp=$SECCOMP_PROFILE" \
        --shm-size=1g \
        -p "127.0.0.1:${HOST_PORT}:3389" \
        "$IMAGE" >/dev/null
fi

echo "Esperando XRDP..."

for i in {1..30}; do
    if docker exec "$CONTAINER" pgrep -x xrdp >/dev/null 2>&1 && \
       docker exec "$CONTAINER" pgrep -x xrdp-sesman >/dev/null 2>&1; then
        sleep 2
        break
    fi

    sleep 1
done

echo "Abriendo Arch Linux + XFCE..."

exec xfreerdp3 \
    /v:127.0.0.1:"$HOST_PORT" \
    /u:arch \
    /dynamic-resolution \
    /clipboard \
    /sound \
    /cert:ignore

