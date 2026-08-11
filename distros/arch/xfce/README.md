# Arch Linux + XFCE en Docker

Entorno gráfico Arch Linux ejecutándose dentro de Docker mediante XRDP.

## Características

- Arch Linux oficial
- XFCE
- XRDP 0.10.6.1
- xorgxrdp 0.10.5
- H.264 mediante x264
- RFX como fallback
- Resolución dinámica
- Clipboard host ↔ contenedor
- Brave Browser
- Chromium Sandbox habilitado
- Seccomp personalizado
- PipeWire
- WirePlumber
- pipewire-pulse
- pipewire-module-xrdp
- Audio mediante RDP
- `/dev/shm` de 1 GB
- XRDP expuesto únicamente en localhost

## Usuario

Usuario:

    arch

Contraseña:

    1234

## Construir imagen

Desde esta carpeta:

    docker buildx build \
      --load \
      --progress=plain \
      -t arch-xfce:1.0.0 \
      .

## Ejecutar

Usar:

    ./launch.sh

O mediante el comando instalado en el host:

    arch-xfce

El launcher:

1. Comprueba que exista la imagen.
2. Crea el contenedor si no existe.
3. Inicia el contenedor si está detenido.
4. Utiliza el perfil seccomp personalizado.
5. Asigna 1 GB a /dev/shm.
6. Publica XRDP en 127.0.0.1:3389.
7. Espera a XRDP y xrdp-sesman.
8. Abre FreeRDP automáticamente.

## FreeRDP

La conexión utiliza:

    /dynamic-resolution
    /clipboard
    /sound
    /cert:ignore

## Seguridad

El contenedor utiliza:

    seccomp-brave.json

No se utiliza:

    --security-opt seccomp=unconfined

Brave mantiene habilitado su sandbox.

Verificado desde:

    brave://sandbox

Resultado esperado:

    You are adequately sandboxed.

## Audio

Flujo:

    Aplicación
        ↓
    PipeWire
        ↓
    pipewire-module-xrdp
        ↓
    XRDP rdpsnd
        ↓
    FreeRDP /sound
        ↓
    Audio del host

No se montan sockets PipeWire/PulseAudio del host.

## Archivos

    Dockerfile
        Construcción reproducible de la imagen.

    start.sh
        Arranque del contenedor.

    startwm.sh
        Inicialización de la sesión XRDP/XFCE.

    start-xfce-xrdp
        Arranque de PipeWire y XFCE por sesión.

    seccomp-brave.json
        Perfil seccomp personalizado para Brave y XFCE.

    launch.sh
        Launcher del host.

## Imagen definitiva

    arch-xfce:1.0.0

## Contenedor definitivo

    arch-xfce

## Puerto

Host:

    127.0.0.1:3389

Contenedor:

    3389

## Estado

Probado correctamente:

- Arranque automático
- Login XRDP
- XFCE
- Resolución dinámica
- Clipboard
- H.264
- Brave
- YouTube
- Audio
- Sandbox de Brave
- Reinicio del contenedor
- Launcher automático
