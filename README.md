# Linux Desktop Containers

Run complete Linux desktop environments inside Docker containers through a simple management interface.

Ejecuta entornos de escritorio Linux completos dentro de contenedores Docker mediante una interfaz de administración sencilla.

**[English](#english) | [Español](#español)**

---

# Español

## Descripción

Linux Desktop Containers es un proyecto para ejecutar distribuciones Linux con entornos de escritorio completos dentro de contenedores Docker.

El proyecto busca ocultar la complejidad de Docker, XRDP y FreeRDP al usuario final. Después de realizar la instalación inicial, las distribuciones disponibles pueden administrarse desde un único comando:

```bash
linux-desktops
```

Desde el administrador se puede instalar, iniciar, detener, actualizar, recrear y desinstalar cada entorno disponible.

Actualmente la primera combinación completamente funcional es:

```text
Arch Linux + XFCE
```

Las demás distribuciones y escritorios incluidos en el catálogo continúan en desarrollo.

---

## Estado del proyecto

| Distribución | Escritorio | Estado |
|---|---|---|
| Arch Linux | XFCE | Disponible |
| Arch Linux | KDE Plasma | Pendiente |
| Arch Linux | GNOME | Pendiente |
| Debian | XFCE | Pendiente |
| Debian | KDE Plasma | Pendiente |
| Debian | GNOME | Pendiente |
| Ubuntu | XFCE | Pendiente |
| Ubuntu | KDE Plasma | Pendiente |
| Ubuntu | GNOME | Pendiente |
| Fedora | XFCE | Pendiente |
| Fedora | KDE Plasma | Pendiente |
| Fedora | GNOME | Pendiente |
| Xubuntu | XFCE | Pendiente |
| Lubuntu | LXQt | Pendiente |

---

## Cómo funciona

Las imágenes Docker no se construyen en la computadora del usuario durante la instalación.

Cada imagen se prepara previamente con la distribución, el escritorio y los componentes necesarios. Una vez validada, se publica en GitHub Container Registry.

El flujo para el usuario es:

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
  v
Asignar puerto RDP local
  |
  v
Crear acceso en el menú de aplicaciones
  |
  v
FreeRDP
  |
  v
XRDP + Xorg
  |
  v
Escritorio Linux
```

Por ejemplo, Arch Linux + XFCE utiliza:

```text
ghcr.io/fartavia3210-design/linux-desktop-containers/arch-xfce:latest
```

La imagen ya contiene el sistema preparado.

Por esta razón, instalar desde Linux Desktop Containers es considerablemente más rápido que construir la imagen desde el Dockerfile. Docker descarga las capas que necesita y crea un contenedor a partir de la imagen existente.

Si las capas ya existen localmente, Docker también puede reutilizarlas.

---

## Funciones actuales

El administrador permite:

- consultar las distribuciones disponibles;
- instalar escritorios;
- descargar imágenes desde GHCR;
- crear contenedores automáticamente;
- iniciar escritorios;
- detener contenedores;
- consultar su estado;
- actualizar imágenes;
- recrear contenedores;
- desinstalar escritorios;
- eliminar opcionalmente la imagen local;
- recrear accesos del menú de aplicaciones;
- comprobar dependencias.

Arch Linux + XFCE incluye además:

- XRDP;
- xorgxrdp;
- Xorg;
- RFX;
- resolución dinámica;
- portapapeles;
- audio;
- PipeWire;
- Brave Browser;
- perfil seccomp personalizado.

---

## Arquitectura del proyecto

La estructura general del repositorio es:

```text
linux-desktop-containers/
├── .github/
│   └── workflows/
├── assets/
├── common/
│   ├── scripts/
│   └── security/
├── distros/
│   ├── arch/
│   ├── debian/
│   ├── fedora/
│   ├── lubuntu/
│   ├── ubuntu/
│   └── xubuntu/
├── launchers/
├── manager/
├── catalog.json
├── install.sh
├── linux-desktops
└── README.md
```

### `catalog.json`

Define las distribuciones y escritorios reconocidos por el administrador.

Entre otros valores, contiene:

- disponibilidad;
- imagen remota;
- nombre del contenedor;
- configuración de puertos;
- memoria compartida;
- usuario RDP;
- perfil seccomp;
- nombre del acceso de aplicaciones.

### `manager/`

Contiene la lógica principal del administrador.

```text
catalog.py
config.py
containers.py
dependencies.py
images.py
installer.py
shortcuts.py
updater.py
```

### `distros/`

Contiene las implementaciones específicas de cada combinación.

Ejemplo:

```text
distros/arch/xfce/
```

Cada combinación puede contener su Dockerfile, scripts de inicio y configuración particular.

### `common/`

Contiene recursos reutilizables entre diferentes imágenes, como perfiles de seguridad y scripts comunes.

### `launchers/`

Contiene el launcher encargado de iniciar el contenedor y establecer la conexión RDP.

---

## Requisitos

Actualmente el flujo de instalación automática ha sido probado principalmente en distribuciones basadas en Arch Linux.

Ejemplos:

```text
Arch Linux
CachyOS
Manjaro
```

Dependencias utilizadas:

- Docker;
- Docker Buildx;
- Python 3;
- Git;
- Bash;
- FreeRDP.

El instalador puede detectar diferentes familias de distribuciones, pero la instalación automática de paquetes está implementada actualmente para `pacman`.

El soporte equivalente para `apt` y `dnf` está pendiente.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/fartavia3210-design/linux-desktop-containers.git
```

### 2. Entrar al directorio

```bash
cd linux-desktop-containers
```

### 3. Ejecutar el instalador

```bash
./install.sh
```

El instalador comprueba el sistema y prepara:

```text
~/.local/bin/linux-desktops
~/.local/bin/linux-desktop-launcher
```

También inicializa los directorios de configuración correspondientes y crea una entrada para Linux Desktop Containers en el menú de aplicaciones.

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

Las funciones de actualización del propio administrador y el panel de configuración todavía se encuentran en desarrollo.

---

## Instalación de un escritorio

Entrar en:

```text
Distribuciones
```

Seleccionar la distribución y posteriormente el escritorio.

Ejemplo:

```text
Arch Linux
└── XFCE
```

El administrador realiza automáticamente:

```text
Comprobar imagen
      |
      v
docker pull
      |
      v
docker create
      |
      v
Configurar puerto y seguridad
      |
      v
Crear acceso de aplicaciones
```

---

## Gestión de escritorios

Para una instalación existente están disponibles actualmente:

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

Consulta la imagen publicada en GHCR.

Si la imagen remota ha cambiado, Docker descarga la nueva versión y el administrador puede recrear el contenedor.

### Recrear contenedor

Elimina el contenedor existente y crea otro a partir de la imagen instalada.

> La persistencia completa del directorio personal todavía no está implementada. Los datos almacenados únicamente dentro del contenedor pueden perderse durante una recreación.

### Desinstalar

Elimina:

- el contenedor;
- el acceso de aplicaciones.

También permite eliminar opcionalmente la imagen Docker almacenada localmente.

---

## Accesos de aplicaciones

Los accesos creados por Linux Desktop Containers se almacenan en:

```text
~/.local/share/applications/
```

Por ejemplo:

```text
linux-desktop-containers-arch-xfce.desktop
```

De esta forma las distribuciones instaladas pueden aparecer en el lanzador de aplicaciones del entorno anfitrión.

---

## Conexión gráfica

La arquitectura gráfica actual utiliza:

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
Entorno de escritorio
```

La configuración estable actual utiliza:

```text
RFX
GDI por software
Dynamic Resolution
Clipboard
Audio
```

---

## Red

Los puertos RDP se publican únicamente sobre la interfaz local:

```text
127.0.0.1
```

Ejemplo:

```text
127.0.0.1:32770 -> 3389/tcp
```

Docker puede asignar automáticamente un puerto diferente para cada contenedor.

El launcher obtiene ese puerto automáticamente antes de iniciar FreeRDP.

No es necesario que el usuario conozca el puerto asignado.

---

## Seguridad

Arch Linux + XFCE utiliza un perfil seccomp personalizado.

El objetivo es habilitar únicamente las operaciones adicionales necesarias para el funcionamiento del escritorio y de las aplicaciones que necesitan mecanismos de sandboxing, sin ejecutar el contenedor completo utilizando `--privileged`.

El servicio RDP se publica exclusivamente sobre localhost y no está pensado para exposición directa a Internet.

---

## Credenciales actuales

La imagen Arch Linux + XFCE utiliza actualmente:

```text
Usuario: arch
Contraseña: 1234
```

El launcher proporciona estas credenciales automáticamente al cliente RDP.

Este mecanismo será sustituido posteriormente por una solución de gestión de credenciales más adecuada.

---

## Configuración local

El proyecto utiliza rutas XDG para separar los datos del usuario del repositorio.

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

Las imágenes pueden construirse y publicarse mediante GitHub Actions.

Para Arch Linux + XFCE:

```text
.github/workflows/publish-arch-xfce.yml
```

Cuando cambia la implementación de Arch XFCE y los cambios llegan a `main`, el workflow puede:

```text
Checkout
   |
   v
Build
   |
   v
Login GHCR
   |
   v
Push
   |
   v
arch-xfce:latest
```

La publicación utiliza el `GITHUB_TOKEN` temporal proporcionado por GitHub Actions.

No es necesario incluir un Personal Access Token en el repositorio.

---

## Limitaciones actuales

Las siguientes funciones continúan pendientes:

- persistencia completa del usuario;
- gestión segura de credenciales;
- actualización automática del administrador;
- panel de configuración;
- instalación automática mediante `apt`;
- instalación automática mediante `dnf`;
- iconos específicos para cada distribución;
- distribuciones y escritorios adicionales.

---

## Imágenes Docker

Las imágenes publicadas pueden descargarse independientemente del administrador.

### Arch Linux

#### XFCE

**Disponible**

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/arch-xfce:latest
```

#### KDE Plasma

**Pendiente**

Imagen todavía no publicada.

#### GNOME

**Pendiente**

Imagen todavía no publicada.

### Debian

#### XFCE

**Pendiente**

Imagen todavía no publicada.

#### KDE Plasma

**Pendiente**

Imagen todavía no publicada.

#### GNOME

**Pendiente**

Imagen todavía no publicada.

### Ubuntu

#### XFCE

**Pendiente**

Imagen todavía no publicada.

#### KDE Plasma

**Pendiente**

Imagen todavía no publicada.

#### GNOME

**Pendiente**

Imagen todavía no publicada.

### Fedora

#### XFCE

**Pendiente**

Imagen todavía no publicada.

#### KDE Plasma

**Pendiente**

Imagen todavía no publicada.

#### GNOME

**Pendiente**

Imagen todavía no publicada.

### Xubuntu

#### XFCE

**Pendiente**

Imagen todavía no publicada.

### Lubuntu

#### LXQt

**Pendiente**

Imagen todavía no publicada.

---

## Desarrollo

Las nuevas implementaciones siguen la estructura:

```text
distros/<distribucion>/<escritorio>/
```

Una vez construida y validada una combinación:

```text
Implementación
      |
      v
Imagen Docker
      |
      v
GitHub Container Registry
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

---

## Licencia

Este proyecto **no se distribuye bajo una licencia de código abierto**.

Copyright © 2026. Todos los derechos reservados.

El código fuente se encuentra disponible públicamente para visualización y referencia. No se concede permiso para copiar, modificar, redistribuir, sublicenciar o crear trabajos derivados sin autorización previa del titular de los derechos.

Consulta el archivo [`LICENSE`](LICENSE) para obtener más información.

---

# English

## Description

Linux Desktop Containers is a project designed to run complete Linux distributions with desktop environments inside Docker containers.

The project aims to hide the complexity of Docker, XRDP and FreeRDP from the end user. After the initial installation, available distributions can be managed through a single command:

```bash
linux-desktops
```

The manager can install, start, stop, update, recreate and uninstall each available desktop environment.

The first fully functional combination currently available is:

```text
Arch Linux + XFCE
```

The remaining distributions and desktop environments included in the catalog are still under development.

---

## Project status

| Distribution | Desktop | Status |
|---|---|---|
| Arch Linux | XFCE | Available |
| Arch Linux | KDE Plasma | Pending |
| Arch Linux | GNOME | Pending |
| Debian | XFCE | Pending |
| Debian | KDE Plasma | Pending |
| Debian | GNOME | Pending |
| Ubuntu | XFCE | Pending |
| Ubuntu | KDE Plasma | Pending |
| Ubuntu | GNOME | Pending |
| Fedora | XFCE | Pending |
| Fedora | KDE Plasma | Pending |
| Fedora | GNOME | Pending |
| Xubuntu | XFCE | Pending |
| Lubuntu | LXQt | Pending |

---

## How it works

Docker images are not built on the user's computer during installation.

Each image is prepared in advance with the distribution, desktop environment and required components. Once validated, it is published to GitHub Container Registry.

The user-side flow is:

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
Download image from GHCR
  |
  v
Create Docker container
  |
  v
Assign local RDP port
  |
  v
Create application launcher
  |
  v
FreeRDP
  |
  v
XRDP + Xorg
  |
  v
Linux desktop
```

For example, Arch Linux + XFCE uses:

```text
ghcr.io/fartavia3210-design/linux-desktop-containers/arch-xfce:latest
```

The image already contains the prepared system.

For this reason, installing through Linux Desktop Containers is considerably faster than building the image from its Dockerfile. Docker downloads the required layers and creates a container from the existing image.

If those layers already exist locally, Docker can reuse them.

---

## Current features

The manager currently supports:

- listing available distributions;
- installing desktops;
- downloading images from GHCR;
- automatically creating containers;
- starting desktops;
- stopping containers;
- checking container status;
- updating images;
- recreating containers;
- uninstalling desktops;
- optionally removing local images;
- recreating application launchers;
- checking dependencies.

Arch Linux + XFCE also includes:

- XRDP;
- xorgxrdp;
- Xorg;
- RFX;
- dynamic resolution;
- clipboard support;
- audio;
- PipeWire;
- Brave Browser;
- a custom seccomp profile.

---

## Project architecture

The general repository structure is:

```text
linux-desktop-containers/
├── .github/
│   └── workflows/
├── assets/
├── common/
│   ├── scripts/
│   └── security/
├── distros/
│   ├── arch/
│   ├── debian/
│   ├── fedora/
│   ├── lubuntu/
│   ├── ubuntu/
│   └── xubuntu/
├── launchers/
├── manager/
├── catalog.json
├── install.sh
├── linux-desktops
└── README.md
```

### `catalog.json`

Defines the distributions and desktop environments recognized by the manager.

It includes information such as:

- availability;
- remote image;
- container name;
- port configuration;
- shared memory;
- RDP user;
- seccomp profile;
- application launcher name.

### `manager/`

Contains the main manager logic.

```text
catalog.py
config.py
containers.py
dependencies.py
images.py
installer.py
shortcuts.py
updater.py
```

### `distros/`

Contains the implementation of each distribution and desktop combination.

Example:

```text
distros/arch/xfce/
```

Each combination can contain its Dockerfile, startup scripts and specific configuration.

### `common/`

Contains reusable resources such as security profiles and common scripts.

### `launchers/`

Contains the launcher responsible for starting containers and establishing RDP connections.

---

## Requirements

The automatic installation flow has currently been tested mainly on Arch-based distributions.

Examples:

```text
Arch Linux
CachyOS
Manjaro
```

Required components include:

- Docker;
- Docker Buildx;
- Python 3;
- Git;
- Bash;
- FreeRDP.

The installer can detect multiple Linux distribution families, but automatic package installation is currently implemented for `pacman`.

Equivalent `apt` and `dnf` support is pending.

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

The installer checks the host system and prepares:

```text
~/.local/bin/linux-desktops
~/.local/bin/linux-desktop-launcher
```

It also initializes the required configuration directories and creates an application launcher for Linux Desktop Containers.

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

The manager self-update feature and advanced configuration panel are still under development.

---

## Installing a desktop

Open:

```text
Distributions
```

Select a distribution followed by a desktop environment.

Example:

```text
Arch Linux
└── XFCE
```

The manager automatically performs:

```text
Check image
    |
    v
docker pull
    |
    v
docker create
    |
    v
Configure port and security
    |
    v
Create application launcher
```

---

## Desktop management

For an installed desktop, the following operations are currently available:

```text
Start / Open desktop
Stop
View status
Update
Recreate container
Uninstall
Recreate application launcher
```

### Update

Checks the image published in GHCR.

If the remote image has changed, Docker downloads the new version and the manager can recreate the container.

### Recreate container

Removes the existing container and creates a new one from the installed image.

> Full home-directory persistence has not yet been implemented. Data stored only inside the container may be lost when recreating it.

### Uninstall

Removes:

- the container;
- the application launcher.

The locally stored Docker image can optionally be removed as well.

---

## Application launchers

Launchers created by Linux Desktop Containers are stored in:

```text
~/.local/share/applications/
```

For example:

```text
linux-desktop-containers-arch-xfce.desktop
```

This allows installed distributions to appear in the host desktop environment's application launcher.

---

## Graphical connection

The current graphical architecture uses:

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
Desktop environment
```

The current stable configuration uses:

```text
RFX
Software GDI
Dynamic Resolution
Clipboard
Audio
```

---

## Networking

RDP ports are published only on the local interface:

```text
127.0.0.1
```

Example:

```text
127.0.0.1:32770 -> 3389/tcp
```

Docker can automatically assign a different host port to each container.

The launcher discovers the assigned port before starting FreeRDP.

The user does not need to know the port number.

---

## Security

Arch Linux + XFCE uses a custom seccomp profile.

Its purpose is to enable only the additional operations required by the desktop environment and applications that depend on sandboxing mechanisms, without running the entire container with `--privileged`.

The RDP service is exposed only through localhost and is not intended to be directly exposed to the Internet.

---

## Current credentials

The Arch Linux + XFCE image currently uses:

```text
Username: arch
Password: 1234
```

The launcher automatically provides these credentials to the RDP client.

This mechanism is expected to be replaced by a more appropriate credential-management solution.

---

## Local configuration

The project uses XDG paths to keep user data separate from the cloned repository.

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

Images can be automatically built and published using GitHub Actions.

Arch Linux + XFCE currently uses:

```text
.github/workflows/publish-arch-xfce.yml
```

When the Arch XFCE implementation changes and reaches `main`, the workflow can:

```text
Checkout
   |
   v
Build
   |
   v
Login to GHCR
   |
   v
Push
   |
   v
arch-xfce:latest
```

Publishing uses the temporary `GITHUB_TOKEN` supplied by GitHub Actions.

A Personal Access Token does not need to be stored in the repository.

---

## Current limitations

The following features are still pending:

- full user-data persistence;
- improved credential management;
- automatic manager self-update;
- configuration panel;
- automatic `apt` dependency installation;
- automatic `dnf` dependency installation;
- distribution-specific icons;
- additional distributions and desktop environments.

---

## Docker images

Published images can also be downloaded independently of the manager.

### Arch Linux

#### XFCE

**Available**

```bash
docker pull ghcr.io/fartavia3210-design/linux-desktop-containers/arch-xfce:latest
```

#### KDE Plasma

**Pending**

Image not published yet.

#### GNOME

**Pending**

Image not published yet.

### Debian

#### XFCE

**Pending**

Image not published yet.

#### KDE Plasma

**Pending**

Image not published yet.

#### GNOME

**Pending**

Image not published yet.

### Ubuntu

#### XFCE

**Pending**

Image not published yet.

#### KDE Plasma

**Pending**

Image not published yet.

#### GNOME

**Pending**

Image not published yet.

### Fedora

#### XFCE

**Pending**

Image not published yet.

#### KDE Plasma

**Pending**

Image not published yet.

#### GNOME

**Pending**

Image not published yet.

### Xubuntu

#### XFCE

**Pending**

Image not published yet.

### Lubuntu

#### LXQt

**Pending**

Image not published yet.

---

## Development

New implementations follow:

```text
distros/<distribution>/<desktop>/
```

Once a combination has been built and validated:

```text
Implementation
      |
      v
Docker image
      |
      v
GitHub Container Registry
      |
      v
catalog.json
      |
      v
available: true
      |
      v
Available through linux-desktops
```

---

## License

This project **is not distributed under an open-source license**.

Copyright © 2026. All rights reserved.

The source code is publicly visible for viewing and reference purposes. No permission is granted to copy, modify, redistribute, sublicense or create derivative works without prior authorization from the copyright holder.

See [`LICENSE`](LICENSE) for additional information.
