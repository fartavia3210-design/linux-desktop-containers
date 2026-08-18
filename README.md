# Linux Desktop Containers

Run complete Linux desktop environments inside Docker containers through a simple management interface.

Ejecuta entornos de escritorio Linux completos dentro de contenedores Docker mediante una interfaz de administración sencilla.

**[English](#english) | [Español](#español)**

---

# Español

## Descripción

Linux Desktop Containers es un proyecto para ejecutar distribuciones Linux con entornos de escritorio completos dentro de contenedores Docker y acceder a ellos mediante RDP.

El objetivo es ocultar al usuario final la complejidad de Docker, XRDP, xorgxrdp y FreeRDP. Después de instalar el administrador, los escritorios disponibles pueden gestionarse desde un único comando:

```bash
linux-desktops
```

Actualmente existen tres combinaciones XFCE funcionales e integradas:

```text
Arch Linux + XFCE
Debian 13 + XFCE
Fedora 44 + XFCE
```

El proyecto mantiene una arquitectura común para contenedores, seguridad, perfiles RDP, accesos de aplicaciones, dependencias y publicación de imágenes, evitando soluciones globales innecesarias cuando un problema pertenece a un host o distribución específica.

---

## Estado del proyecto

| Distribución | Escritorio | Estado |
|---|---|---|
| Arch Linux | XFCE | ✅ Disponible |
| Arch Linux | KDE Plasma | Pendiente |
| Arch Linux | GNOME | Pendiente |
| Debian | XFCE | ✅ Disponible |
| Debian | KDE Plasma | Pendiente |
| Debian | GNOME | Pendiente |
| Ubuntu | XFCE | Pendiente |
| Ubuntu | KDE Plasma | Pendiente |
| Ubuntu | GNOME | Pendiente |
| Fedora | XFCE | ✅ Disponible |
| Fedora | KDE Plasma | Pendiente |
| Fedora | GNOME | Pendiente |
| Xubuntu | XFCE | Pendiente |
| Lubuntu | LXQt | Pendiente |

---

## Imágenes disponibles

### Arch Linux + XFCE

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/arch-xfce:latest
```

```text
Contenedor: ldc-arch-xfce
Usuario RDP: arch
Contraseña: 1234
```

### Debian 13 + XFCE

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/debian-xfce:latest
```

```text
Contenedor: ldc-debian-xfce
Usuario RDP: debian
Contraseña: 1234
```

### Fedora 44 + XFCE

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/fedora-xfce:latest
```

```text
Contenedor: ldc-fedora-xfce
Usuario RDP: fedora
Contraseña: 1234
```

> Las credenciales están actualmente definidas en el catálogo para simplificar la etapa de desarrollo. Se planea sustituir este mecanismo por una gestión de credenciales más adecuada.

---

## Funciones actuales

El administrador permite:

- detectar el sistema anfitrión;
- detectar dependencias;
- instalar dependencias mediante `pacman`, `apt` o `dnf`;
- comprobar Docker y Docker Buildx;
- detectar FreeRDP;
- listar distribuciones y escritorios;
- descargar imágenes desde GHCR;
- crear contenedores automáticamente;
- asignar puertos RDP dinámicos;
- iniciar escritorios;
- detener contenedores;
- consultar su estado;
- actualizar imágenes;
- recrear contenedores;
- desinstalar escritorios;
- eliminar opcionalmente imágenes locales;
- crear y recrear accesos en el menú de aplicaciones;
- aplicar perfiles de seguridad según el host;
- seleccionar perfiles RDP según el catálogo y el host.

---

## Cómo funciona

Las imágenes Docker se preparan previamente con la distribución, el escritorio y los componentes necesarios.

```text
GitHub
  |
  | clone
  v
Repositorio local
  |
  | ./install.sh
  v
Linux Desktop Containers
  |
  | linux-desktops
  v
Seleccionar distribución
  |
  v
Seleccionar escritorio
  |
  v
Descargar imagen desde GHCR
  |
  v
Crear contenedor Docker
  |
  +--> seguridad del host
  +--> seccomp
  +--> /dev/shm
  +--> puerto RDP local dinámico
  |
  v
Crear acceso de aplicaciones
  |
  v
FreeRDP
  |
  v
XRDP
  |
  v
xorgxrdp + Xorg
  |
  v
Escritorio Linux
```

Durante una instalación normal las imágenes no necesitan construirse localmente. Docker descarga las capas publicadas en GHCR y reutiliza capas existentes cuando es posible.

---

## Arquitectura gráfica

```text
FreeRDP
   |
   v
XRDP
   |
   v
xorgxrdp
   |
   v
Xorg
   |
   v
XFCE
```

La conexión se resuelve mediante perfiles RDP declarativos definidos en `catalog.json`.

### Perfil `standard`

```text
/dynamic-resolution
/clipboard
/sound
/cert:ignore
```

Es el perfil normal para las combinaciones que funcionan correctamente con la ruta gráfica predeterminada de XRDP/FreeRDP.

### Perfil `compat-rfx`

```text
/gfx:RFX
/gdi:sw
/dynamic-resolution
/clipboard
/sound
/cert:ignore
```

Es una ruta de compatibilidad basada en RemoteFX y GDI por software.

### Selección actual de perfiles

| Escritorio | Perfil predeterminado | Excepciones |
|---|---|---|
| Arch Linux + XFCE | `compat-rfx` | Ninguna actualmente |
| Debian + XFCE | `standard` | Host Arch Linux puro → `compat-rfx` |
| Fedora + XFCE | `standard` | Ninguna actualmente |

La resolución se realiza en `manager/rdp_profiles.py`.

Los overrides de host se aplican por el `ID` exacto de la distribución anfitriona. El workaround de Arch puro no se aplica automáticamente a todas las distribuciones derivadas de Arch.

---

## Audio

Las imágenes XFCE disponibles incorporan audio remoto mediante PipeWire y XRDP.

```text
Aplicaciones
   |
   v
PipeWire / pipewire-pulse
   |
   v
WirePlumber
   |
   v
pipewire-module-xrdp
   |
   +--> xrdp-sink
   |
   +--> xrdp-source
   |
   v
FreeRDP /sound
```

Esto permite que el audio reproducido dentro del contenedor se escuche en el host.

Fedora 44 + XFCE inicia PipeWire, `pipewire-pulse` y WirePlumber dentro de la sesión XRDP y utiliza el autostart de `pipewire-module-xrdp` para cargar los dispositivos XRDP.

---

## Brave Browser y sandbox

Las imágenes XFCE disponibles incluyen Brave Browser.

Brave se ejecuta con su sandbox real. El proyecto no depende de:

```text
--no-sandbox
--privileged
seccomp=unconfined
```

El perfil compartido:

```text
common/security/seccomp-brave.json
```

permite las operaciones adicionales necesarias para Chromium/Brave sin desactivar globalmente seccomp.

Las imágenes se crean con:

```text
--shm-size=1g
```

para evitar problemas de Chromium/Brave con el `/dev/shm` predeterminado de Docker.

Las pruebas con `brave://sandbox` han confirmado las principales capas de sandbox, incluyendo namespaces y Seccomp-BPF.

---

## Seguridad del host

Linux Desktop Containers adapta la creación del contenedor al sistema de seguridad del host.

### Seccomp

Las combinaciones disponibles utilizan:

```text
common/security/seccomp-brave.json
```

El perfil se aplica únicamente al contenedor correspondiente.

### AppArmor

Si AppArmor está habilitado y la combinación define un perfil, el administrador utiliza:

```text
--security-opt apparmor=linux-desktop-containers
```

Esto mantiene AppArmor habilitado globalmente en el host.

### SELinux

Si el host utiliza SELinux en modo Enforcing, el administrador añade únicamente al contenedor:

```text
--security-opt label=disable
```

Esto desactiva el etiquetado SELinux para ese contenedor, pero **no desactiva SELinux en el host**.

### Sin SELinux ni AppArmor

Si ninguno de los dos mecanismos está activo, no se añade una opción LSM adicional.

---

## Compatibilidad del host

El administrador reconoce estas familias:

| Familia | Gestor de paquetes |
|---|---|
| Arch Linux / CachyOS / Manjaro | `pacman` |
| Debian / Ubuntu y derivados | `apt` |
| Fedora y derivados | `dnf` |

La instalación automática de dependencias está implementada para los tres gestores.

La arquitectura ha sido probada en distintos hosts Linux, incluyendo Arch Linux, CachyOS, Debian y Fedora. La ruta Ubuntu/AppArmor también forma parte de la compatibilidad del proyecto.

### Nota sobre Arch Linux puro

En Arch Linux puro se detectó una incompatibilidad de la ruta H.264/VAAPI del cliente FreeRDP en determinadas conexiones, produciendo pantalla negra.

La ruta comprobada de compatibilidad es:

```text
/gfx:RFX
/gdi:sw
```

Por esta razón Debian XFCE cambia automáticamente a `compat-rfx` cuando el `ID` exacto del host es `arch`.

---

## Red

El puerto RDP de cada contenedor se publica exclusivamente sobre localhost:

```text
127.0.0.1
```

Ejemplo:

```text
127.0.0.1:32770 -> 3389/tcp
```

Docker puede asignar un puerto diferente a cada contenedor.

El launcher obtiene automáticamente el puerto publicado antes de iniciar FreeRDP, por lo que el usuario no necesita conocerlo manualmente.

El diseño actual está orientado a acceso local. No se recomienda exponer XRDP directamente a Internet.

---

## Estructura del repositorio

```text
linux-desktop-containers/
├── .github/
│   └── workflows/
│       ├── publish-arch-xfce.yml
│       ├── publish-debian-xfce.yml
│       └── publish-fedora-xfce.yml
├── assets/
├── common/
│   ├── scripts/
│   └── security/
│       └── seccomp-brave.json
├── distros/
│   ├── arch/
│   │   └── xfce/
│   ├── debian/
│   │   └── xfce/
│   ├── fedora/
│   │   └── xfce/
│   ├── lubuntu/
│   ├── ubuntu/
│   └── xubuntu/
├── launchers/
│   └── desktop-launcher
├── manager/
│   ├── catalog.py
│   ├── config.py
│   ├── containers.py
│   ├── dependencies.py
│   ├── images.py
│   ├── installer.py
│   ├── rdp_profiles.py
│   ├── shortcuts.py
│   └── updater.py
├── catalog.json
├── install.sh
├── linux-desktops
├── LICENSE
└── README.md
```

### `catalog.json`

Es la fuente declarativa principal para:

- distribuciones;
- escritorios;
- disponibilidad;
- imágenes remotas;
- contextos de build;
- nombres de contenedores;
- puertos;
- tamaño de memoria compartida;
- credenciales RDP actuales;
- perfiles RDP;
- overrides por host;
- perfiles seccomp;
- perfiles AppArmor;
- nombres de accesos de aplicaciones.

### `manager/`

Contiene la lógica reutilizable del administrador para detección del host, dependencias, ciclo de vida de contenedores, seguridad, imágenes, instalación, actualización, accesos y perfiles RDP.

### `distros/`

Cada implementación utiliza:

```text
distros/<distribucion>/<escritorio>/
```

Por ejemplo:

```text
distros/fedora/xfce/
```

Cada combinación puede contener su `Dockerfile`, scripts de inicio y configuración específica.

### `common/`

Contiene recursos compartidos entre imágenes, como el perfil seccomp de Brave.

---

## Requisitos

El administrador utiliza:

- Docker;
- Docker Buildx;
- Python 3;
- Git;
- Bash;
- FreeRDP.

El propio administrador puede detectar dependencias faltantes y generar un plan de instalación para `pacman`, `apt` y `dnf`.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/fartavia3210-design/linux-desktop-containers.git
```

### 2. Entrar al proyecto

```bash
cd linux-desktop-containers
```

### 3. Ejecutar el instalador

```bash
./install.sh
```

El instalador prepara, entre otros:

```text
~/.local/bin/linux-desktops
~/.local/bin/linux-desktop-launcher
```

También inicializa los directorios de configuración y crea la entrada principal del proyecto en el menú de aplicaciones.

---

## Uso

Ejecutar:

```bash
linux-desktops
```

Menú principal:

```text
Linux Desktop Containers

1) Distribuciones
2) Escritorios instalados
3) Dependencias
4) Actualizar administrador
5) Configuración
0) Salir
```

Las funciones avanzadas de autoactualización del administrador y configuración continúan en desarrollo.

---

## Instalación de un escritorio

Entrar en:

```text
Distribuciones
```

Seleccionar una distribución y posteriormente un escritorio disponible.

Ejemplos:

```text
Arch Linux
└── XFCE
```

```text
Debian
└── XFCE
```

```text
Fedora
└── XFCE
```

El administrador realiza:

```text
Comprobar imagen
      |
      v
docker pull
      |
      v
docker create
      |
      +--> --shm-size
      +--> seccomp
      +--> AppArmor / SELinux según host
      +--> puerto local dinámico
      |
      v
Crear acceso de aplicaciones
```

---

## Gestión de escritorios

Para una instalación existente están disponibles:

```text
Iniciar / Abrir escritorio
Detener
Ver estado
Actualizar
Recrear contenedor
Desinstalar
Recrear acceso directo
```

### Actualizar

Consulta la imagen remota publicada en GHCR. Si existe una versión nueva, Docker descarga las capas necesarias y el contenedor puede recrearse usando la imagen actualizada.

### Recrear contenedor

Elimina el contenedor existente y crea otro a partir de la imagen instalada.

> La persistencia completa del directorio personal todavía no está implementada. Los datos almacenados exclusivamente dentro del contenedor pueden perderse durante una recreación.

### Desinstalar

Elimina el contenedor y su acceso de aplicaciones. También permite eliminar opcionalmente la imagen Docker local.

---

## Accesos de aplicaciones

Los accesos creados por Linux Desktop Containers se almacenan en:

```text
~/.local/share/applications/
```

Ejemplos:

```text
linux-desktop-containers-arch-xfce.desktop
linux-desktop-containers-debian-xfce.desktop
linux-desktop-containers-fedora-xfce.desktop
```

---

## Configuración local

Configuración:

```text
~/.config/linux-desktop-containers/
```

Datos:

```text
~/.local/share/linux-desktop-containers/
```

Estado:

```text
~/.local/state/linux-desktop-containers/
```

---

## Publicación de imágenes

Las imágenes se construyen y publican mediante GitHub Actions y GitHub Container Registry.

Workflows:

```text
.github/workflows/publish-arch-xfce.yml
.github/workflows/publish-debian-xfce.yml
.github/workflows/publish-fedora-xfce.yml
```

```text
Push a main
   |
   v
GitHub Actions
   |
   v
Checkout
   |
   v
Login GHCR
   |
   v
docker build
   |
   v
docker push
   |
   v
ghcr.io/fartavia3210-design/linux-desktop-containers/<imagen>:latest
```

La publicación utiliza el `GITHUB_TOKEN` temporal proporcionado por GitHub Actions. No es necesario almacenar un Personal Access Token en el repositorio.

---

## Notas de las implementaciones actuales

### Arch Linux + XFCE

- Base rolling de Arch Linux.
- XRDP + xorgxrdp.
- PipeWire.
- Brave Browser con sandbox.
- `--shm-size=1g`.
- Perfil RDP actual: `compat-rfx`.
- Perfil seccomp compartido.

### Debian 13 + XFCE

- Base Debian 13.
- XRDP 0.10.x + xorgxrdp.
- PipeWire, WirePlumber y audio XRDP.
- Brave Browser con sandbox.
- `--shm-size=1g`.
- Perfil RDP normal: `standard`.
- Override exacto para host Arch puro: `compat-rfx`.
- `light-locker` deshabilitado en la sesión XRDP para evitar fallos del locker dentro del contenedor.

### Fedora 44 + XFCE

- Base Fedora 44.
- Paquetes Fedora de XRDP y xorgxrdp.
- XFCE 4.20.
- PipeWire + WirePlumber + `pipewire-module-xrdp`.
- Brave Browser mediante repositorio RPM oficial.
- Brave con sandbox real utilizando el perfil seccomp compartido.
- `--shm-size=1g`.
- Perfil RDP: `standard`.
- `xfce-polkit` gráfico deshabilitado en autostart para sesiones XRDP dentro del contenedor; `polkitd` permanece disponible.
- Rendimiento gráfico fluido con la configuración estándar.

---

## Limitaciones actuales

Continúan pendientes:

- persistencia completa del directorio personal;
- gestión segura y configurable de credenciales;
- panel de configuración completo;
- actualización totalmente automática del administrador;
- iconos específicos para todas las distribuciones;
- más escritorios y distribuciones;
- una arquitectura formal para acceso remoto más allá del modo localhost actual.

---

## Desarrollo

Las nuevas implementaciones siguen:

```text
distros/<distribucion>/<escritorio>/
```

Flujo recomendado:

```text
Implementación experimental
        |
        v
Pruebas locales
        |
        v
Validación de XRDP
        |
        +--> video
        +--> resolución dinámica
        +--> clipboard
        +--> audio
        +--> sandbox
        +--> seguridad del host
        |
        v
Integración en distros/
        |
        v
Workflow GHCR
        |
        v
catalog.json
        |
        v
available: true
        |
        v
Disponible en linux-desktops
```

Los cambios compartidos deben conservar la compatibilidad entre hosts y evitar workarounds globales cuando el problema pertenece a una distribución o entorno específico.

---

## Licencia

Este proyecto **no se distribuye bajo una licencia de código abierto**.

Copyright © 2026. Todos los derechos reservados.

El código fuente se encuentra disponible públicamente para visualización y referencia. No se concede permiso para copiar, modificar, redistribuir, sublicenciar o crear trabajos derivados sin autorización previa del titular de los derechos.

Consulta [`LICENSE`](LICENSE) para más información.

---

# English

## Description

Linux Desktop Containers is a project for running complete Linux distributions with desktop environments inside Docker containers and accessing them through RDP.

Its goal is to hide the complexity of Docker, XRDP, xorgxrdp and FreeRDP from the end user. After installing the manager, available desktops can be controlled through a single command:

```bash
linux-desktops
```

There are currently three functional and integrated XFCE combinations:

```text
Arch Linux + XFCE
Debian 13 + XFCE
Fedora 44 + XFCE
```

The project uses a shared architecture for containers, security, RDP profiles, application launchers, dependencies and image publishing while avoiding unnecessary global workarounds for host-specific or distribution-specific issues.

---

## Project status

| Distribution | Desktop | Status |
|---|---|---|
| Arch Linux | XFCE | ✅ Available |
| Arch Linux | KDE Plasma | Pending |
| Arch Linux | GNOME | Pending |
| Debian | XFCE | ✅ Available |
| Debian | KDE Plasma | Pending |
| Debian | GNOME | Pending |
| Ubuntu | XFCE | Pending |
| Ubuntu | KDE Plasma | Pending |
| Ubuntu | GNOME | Pending |
| Fedora | XFCE | ✅ Available |
| Fedora | KDE Plasma | Pending |
| Fedora | GNOME | Pending |
| Xubuntu | XFCE | Pending |
| Lubuntu | LXQt | Pending |

---

## Available images

### Arch Linux + XFCE

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/arch-xfce:latest
```

```text
Container: ldc-arch-xfce
RDP user: arch
Password: 1234
```

### Debian 13 + XFCE

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/debian-xfce:latest
```

```text
Container: ldc-debian-xfce
RDP user: debian
Password: 1234
```

### Fedora 44 + XFCE

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/fedora-xfce:latest
```

```text
Container: ldc-fedora-xfce
RDP user: fedora
Password: 1234
```

> Credentials are currently defined in the catalog to simplify the development stage. This mechanism is expected to be replaced by a more appropriate credential-management solution.

---

## Current features

The manager supports:

- host distribution detection;
- dependency detection;
- automatic dependency installation through `pacman`, `apt` or `dnf`;
- Docker and Docker Buildx checks;
- FreeRDP detection;
- listing distributions and desktops;
- pulling images from GHCR;
- automatic container creation;
- dynamic RDP host ports;
- starting desktops;
- stopping containers;
- checking container status;
- updating images;
- recreating containers;
- uninstalling desktops;
- optionally removing local images;
- creating and recreating application launchers;
- host-aware security options;
- host-aware declarative RDP profiles.

---

## How it works

Docker images are prepared in advance with the distribution, desktop environment and required components.

```text
GitHub
  |
  | clone
  v
Local repository
  |
  | ./install.sh
  v
Linux Desktop Containers
  |
  | linux-desktops
  v
Select distribution
  |
  v
Select desktop
  |
  v
Pull image from GHCR
  |
  v
Create Docker container
  |
  +--> host security
  +--> seccomp
  +--> /dev/shm
  +--> dynamic local RDP port
  |
  v
Create application launcher
  |
  v
FreeRDP
  |
  v
XRDP
  |
  v
xorgxrdp + Xorg
  |
  v
Linux desktop
```

Images do not need to be built locally during normal installation. Docker downloads the published layers from GHCR and reuses existing layers whenever possible.

---

## Graphics architecture

```text
FreeRDP
   |
   v
XRDP
   |
   v
xorgxrdp
   |
   v
Xorg
   |
   v
XFCE
```

RDP connections are resolved through declarative profiles defined in `catalog.json`.

### `standard` profile

```text
/dynamic-resolution
/clipboard
/sound
/cert:ignore
```

This is the normal profile for combinations that work correctly with the default XRDP/FreeRDP graphics path.

### `compat-rfx` profile

```text
/gfx:RFX
/gdi:sw
/dynamic-resolution
/clipboard
/sound
/cert:ignore
```

This is a compatibility path based on RemoteFX and software GDI.

### Current profile selection

| Desktop | Default profile | Exceptions |
|---|---|---|
| Arch Linux + XFCE | `compat-rfx` | None currently |
| Debian + XFCE | `standard` | Pure Arch Linux host → `compat-rfx` |
| Fedora + XFCE | `standard` | None currently |

Profile resolution is handled by `manager/rdp_profiles.py`.

Host overrides use the exact host distribution `ID`, so the pure Arch workaround is not automatically applied to every Arch-derived distribution.

---

## Audio

Available XFCE images include XRDP audio redirection through PipeWire.

```text
Applications
   |
   v
PipeWire / pipewire-pulse
   |
   v
WirePlumber
   |
   v
pipewire-module-xrdp
   |
   +--> xrdp-sink
   |
   +--> xrdp-source
   |
   v
FreeRDP /sound
```

This allows sound generated inside the container to be played on the host.

Fedora 44 + XFCE starts PipeWire, `pipewire-pulse` and WirePlumber inside the XRDP session and uses the `pipewire-module-xrdp` autostart entry to load the XRDP devices.

---

## Brave Browser and sandboxing

Available XFCE images include Brave Browser.

Brave runs with its real Linux sandbox. The project does not rely on:

```text
--no-sandbox
--privileged
seccomp=unconfined
```

The shared profile:

```text
common/security/seccomp-brave.json
```

allows the additional operations required by Chromium/Brave without globally disabling seccomp.

Containers use:

```text
--shm-size=1g
```

to avoid Chromium/Brave issues caused by Docker's small default `/dev/shm`.

Testing with `brave://sandbox` has confirmed the main sandbox layers, including namespaces and Seccomp-BPF.

---

## Host security

Linux Desktop Containers adapts container creation to the host security system.

### Seccomp

Available combinations use:

```text
common/security/seccomp-brave.json
```

The profile is applied only to the corresponding container.

### AppArmor

When AppArmor is enabled and the desktop entry defines a profile, the manager uses:

```text
--security-opt apparmor=linux-desktop-containers
```

This keeps AppArmor enabled globally on the host.

### SELinux

When the host uses SELinux in Enforcing mode, the manager adds only to the container:

```text
--security-opt label=disable
```

This disables SELinux labeling for that container but **does not disable SELinux on the host**.

### Hosts without SELinux or AppArmor

No additional LSM option is added.

---

## Host compatibility

The manager recognizes these Linux families:

| Family | Package manager |
|---|---|
| Arch Linux / CachyOS / Manjaro | `pacman` |
| Debian / Ubuntu and derivatives | `apt` |
| Fedora and derivatives | `dnf` |

Automatic dependency installation is implemented for all three.

The architecture has been tested on multiple Linux hosts, including Arch Linux, CachyOS, Debian and Fedora. The Ubuntu/AppArmor path is also part of the project's compatibility work.

### Pure Arch Linux note

On pure Arch Linux, an incompatibility was observed in the FreeRDP H.264/VAAPI graphics path for some connections, causing a black screen.

The validated compatibility path is:

```text
/gfx:RFX
/gdi:sw
```

For this reason Debian XFCE automatically switches to `compat-rfx` when the host's exact `ID` is `arch`.

---

## Networking

Each container's RDP port is bound only to localhost:

```text
127.0.0.1
```

Example:

```text
127.0.0.1:32770 -> 3389/tcp
```

Docker can assign a different host port to each container.

The launcher automatically discovers the published port before starting FreeRDP, so the user does not need to know it manually.

The current design is local-first. Directly exposing XRDP to the Internet is not recommended.

---

## Repository structure

```text
linux-desktop-containers/
├── .github/
│   └── workflows/
│       ├── publish-arch-xfce.yml
│       ├── publish-debian-xfce.yml
│       └── publish-fedora-xfce.yml
├── assets/
├── common/
│   ├── scripts/
│   └── security/
│       └── seccomp-brave.json
├── distros/
│   ├── arch/
│   │   └── xfce/
│   ├── debian/
│   │   └── xfce/
│   ├── fedora/
│   │   └── xfce/
│   ├── lubuntu/
│   ├── ubuntu/
│   └── xubuntu/
├── launchers/
│   └── desktop-launcher
├── manager/
│   ├── catalog.py
│   ├── config.py
│   ├── containers.py
│   ├── dependencies.py
│   ├── images.py
│   ├── installer.py
│   ├── rdp_profiles.py
│   ├── shortcuts.py
│   └── updater.py
├── catalog.json
├── install.sh
├── linux-desktops
├── LICENSE
└── README.md
```

### `catalog.json`

The main declarative source for distributions, desktops, availability, remote images, build contexts, container names, ports, shared memory, current credentials, RDP profiles, host overrides, security profiles and application-launcher names.

### `manager/`

Contains reusable manager logic for host detection, dependencies, container lifecycle, security, images, installation, updates, application launchers and RDP profile resolution.

### `distros/`

Each implementation follows:

```text
distros/<distribution>/<desktop>/
```

For example:

```text
distros/fedora/xfce/
```

Each combination can contain its `Dockerfile`, startup scripts and specific configuration.

### `common/`

Contains reusable resources shared by multiple images, such as the Brave seccomp profile.

---

## Requirements

The manager uses:

- Docker;
- Docker Buildx;
- Python 3;
- Git;
- Bash;
- FreeRDP.

The manager can detect missing dependencies and build an installation plan for `pacman`, `apt` and `dnf`.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/fartavia3210-design/linux-desktop-containers.git
```

### 2. Enter the project directory

```bash
cd linux-desktop-containers
```

### 3. Run the installer

```bash
./install.sh
```

The installer prepares, among others:

```text
~/.local/bin/linux-desktops
~/.local/bin/linux-desktop-launcher
```

It also initializes the configuration directories and creates the main Linux Desktop Containers application entry.

---

## Usage

Run:

```bash
linux-desktops
```

Main menu:

```text
Linux Desktop Containers

1) Distributions
2) Installed desktops
3) Dependencies
4) Update manager
5) Configuration
0) Exit
```

Advanced manager self-update and configuration features are still under development.

---

## Installing a desktop

Open:

```text
Distributions
```

Select a distribution and then an available desktop.

Examples:

```text
Arch Linux
└── XFCE
```

```text
Debian
└── XFCE
```

```text
Fedora
└── XFCE
```

The manager performs:

```text
Check image
      |
      v
docker pull
      |
      v
docker create
      |
      +--> --shm-size
      +--> seccomp
      +--> AppArmor / SELinux based on host
      +--> dynamic local port
      |
      v
Create application launcher
```

---

## Desktop management

For an installed desktop, the current actions are:

```text
Start / Open desktop
Stop
Show status
Update
Recreate container
Uninstall
Recreate application launcher
```

### Update

Checks the image published to GHCR. If the remote image has changed, Docker downloads the required layers and the container can be recreated with the updated image.

### Recreate container

Removes the current container and creates a new one from the installed image.

> Full home-directory persistence is not implemented yet. Data stored only inside the container can be lost when recreating it.

### Uninstall

Removes the container and its application launcher. It can also optionally remove the local Docker image.

---

## Application launchers

Generated application launchers are stored in:

```text
~/.local/share/applications/
```

Examples:

```text
linux-desktop-containers-arch-xfce.desktop
linux-desktop-containers-debian-xfce.desktop
linux-desktop-containers-fedora-xfce.desktop
```

---

## Local configuration

Configuration:

```text
~/.config/linux-desktop-containers/
```

Data:

```text
~/.local/share/linux-desktop-containers/
```

State:

```text
~/.local/state/linux-desktop-containers/
```

---

## Image publishing

Images are built and published through GitHub Actions and GitHub Container Registry.

Workflows:

```text
.github/workflows/publish-arch-xfce.yml
.github/workflows/publish-debian-xfce.yml
.github/workflows/publish-fedora-xfce.yml
```

```text
Push to main
   |
   v
GitHub Actions
   |
   v
Checkout
   |
   v
Login to GHCR
   |
   v
docker build
   |
   v
docker push
   |
   v
ghcr.io/fartavia3210-design/linux-desktop-containers/<image>:latest
```

Publishing uses the temporary `GITHUB_TOKEN` provided by GitHub Actions. No Personal Access Token needs to be stored in the repository.

---

## Current implementation notes

### Arch Linux + XFCE

- Rolling Arch Linux base.
- XRDP + xorgxrdp.
- PipeWire.
- Brave Browser with sandboxing.
- `--shm-size=1g`.
- Current RDP profile: `compat-rfx`.
- Shared seccomp profile.

### Debian 13 + XFCE

- Debian 13 base.
- XRDP 0.10.x + xorgxrdp.
- PipeWire, WirePlumber and XRDP audio.
- Brave Browser with sandboxing.
- `--shm-size=1g`.
- Normal RDP profile: `standard`.
- Exact pure-Arch host override: `compat-rfx`.
- `light-locker` is disabled in XRDP sessions to avoid locker failures inside the container.

### Fedora 44 + XFCE

- Fedora 44 base.
- Fedora XRDP and xorgxrdp packages.
- XFCE 4.20.
- PipeWire + WirePlumber + `pipewire-module-xrdp`.
- Brave Browser from the official RPM repository.
- Brave uses the shared seccomp profile and retains its real sandbox.
- `--shm-size=1g`.
- RDP profile: `standard`.
- The graphical `xfce-polkit` agent is disabled from XRDP autostart while `polkitd` remains available.
- Smooth graphics performance with the standard configuration.

---

## Current limitations

Still pending:

- full home-directory persistence;
- secure and configurable credential management;
- complete configuration panel;
- fully automatic manager updates;
- distribution-specific icons for every desktop;
- additional distributions and desktop environments;
- a formal remote-access architecture beyond the current localhost-first mode.

---

## Development

New implementations follow:

```text
distros/<distribution>/<desktop>/
```

Recommended flow:

```text
Experimental implementation
        |
        v
Local testing
        |
        v
XRDP validation
        |
        +--> graphics
        +--> dynamic resolution
        +--> clipboard
        +--> audio
        +--> sandbox
        +--> host security
        |
        v
Integration into distros/
        |
        v
GHCR workflow
        |
        v
catalog.json
        |
        v
available: true
        |
        v
Available in linux-desktops
```

Shared changes should preserve host compatibility and avoid global workarounds when an issue belongs only to a specific distribution or environment.

---

## License

This project is **not distributed under an open-source license**.

Copyright © 2026. All rights reserved.

The source code is publicly available for viewing and reference. No permission is granted to copy, modify, redistribute, sublicense or create derivative works without prior authorization from the copyright holder.

See [`LICENSE`](LICENSE) for more information.
