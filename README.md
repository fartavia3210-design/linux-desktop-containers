<div align="center">

# 🐧 Linux Desktop Containers

### Escritorios Linux completos dentro de Docker, accesibles por XRDP  
### Full Linux desktop environments inside Docker, accessible through XRDP

[![Docker](https://img.shields.io/badge/Docker-Engine-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Linux](https://img.shields.io/badge/Host-Linux-FCC624?logo=linux&logoColor=black)](https://www.kernel.org/)
[![FreeRDP](https://img.shields.io/badge/Client-FreeRDP-2C3E50)](https://www.freerdp.com/)
[![Status](https://img.shields.io/badge/status-in%20development-orange)](#-estado-del-proyecto--project-status)

**[🇪🇸 Español](#-español) · [🇬🇧 English](#-english)**

</div>

---

# 🇪🇸 Español

## ✨ ¿Qué es este proyecto?

**Linux Desktop Containers** es una colección de entornos Linux gráficos ejecutados dentro de contenedores Docker.

La idea es poder elegir una distribución y un entorno de escritorio desde un menú sencillo, iniciar el contenedor y abrir automáticamente una sesión gráfica mediante **XRDP + FreeRDP**, sin tener que crear una máquina virtual completa.

```text
Distribución
    ↓
Entorno de escritorio
    ↓
Docker
    ↓
XRDP + H.264
    ↓
FreeRDP
    ↓
Escritorio Linux
```

### 🎯 Objetivo

Mantener en un único repositorio diferentes combinaciones de:

- Arch Linux
- Debian
- Ubuntu
- Fedora
- Xubuntu
- Lubuntu

con escritorios enfocados actualmente en:

- XFCE
- KDE Plasma
- GNOME
- LXQt únicamente para Lubuntu

---

## 🚦 Estado del proyecto / Project status

> [!IMPORTANT]
> El proyecto está en desarrollo. Actualmente **Arch Linux + XFCE** es la primera combinación integrada y validada.

| Distribución | XFCE | KDE Plasma | GNOME | LXQt |
|---|:---:|:---:|:---:|:---:|
| Arch Linux | ✅ Disponible | 🕒 Próximamente | 🕒 Próximamente | — |
| Debian | 🕒 Próximamente | 🕒 Próximamente | 🕒 Próximamente | — |
| Ubuntu | 🕒 Próximamente | 🕒 Próximamente | 🕒 Próximamente | — |
| Fedora | 🕒 Próximamente | 🕒 Próximamente | 🕒 Próximamente | — |
| Xubuntu | 🕒 Próximamente | — | — | — |
| Lubuntu | — | — | — | 🕒 Próximamente |

---

## 🖥️ Arch Linux + XFCE

La implementación actual incluye:

- ✅ Arch Linux oficial
- ✅ XFCE
- ✅ XRDP 0.10.6.1
- ✅ xorgxrdp 0.10.5
- ✅ H.264 mediante x264
- ✅ RFX como fallback
- ✅ Resolución dinámica
- ✅ Portapapeles host ↔ contenedor
- ✅ Brave Browser
- ✅ Sandbox de Chromium habilitado
- ✅ Perfil seccomp personalizado
- ✅ PipeWire + WirePlumber + pipewire-pulse
- ✅ pipewire-module-xrdp
- ✅ Audio mediante RDP
- ✅ `/dev/shm` de 1 GB
- ✅ XRDP publicado únicamente en `127.0.0.1`

Brave, YouTube, audio, sandbox, clipboard y resolución dinámica fueron probados en la implementación actual.

---

## 📦 Dependencias

| Dependencia | Uso |
|---|---|
| **Docker Engine** | Ejecutar contenedores |
| **Docker Buildx** | Construir imágenes |
| **FreeRDP 3** | Abrir la sesión gráfica |
| **Python 3** | Ejecutar `linux-desktops` |
| **Git** | Clonar y actualizar el proyecto |
| **Bash** | Ejecutar los launchers |

El launcher actual utiliza:

```text
xfreerdp3
```

<details>
<summary><strong>📦 Arch Linux / CachyOS</strong></summary>

```bash
sudo pacman -S --needed docker docker-buildx freerdp python git
sudo systemctl enable --now docker
```

Opcionalmente, para usar Docker sin `sudo`:

```bash
sudo usermod -aG docker "$USER"
```

Después cierra sesión y vuelve a entrar.

> [!WARNING]
> El grupo `docker` otorga privilegios equivalentes a root sobre el daemon de Docker.

</details>

<details>
<summary><strong>📦 Debian / Ubuntu / Fedora y otros hosts Linux</strong></summary>

Instala **Docker Engine + Docker Buildx** siguiendo la documentación oficial de Docker para tu distribución.

También necesitas:

- Git
- Python 3
- Bash
- FreeRDP 3 con cliente X11 (`xfreerdp3`)

En Ubuntu moderno, el cliente X11 de FreeRDP 3 está disponible mediante `freerdp3-x11`.

Los nombres exactos de los paquetes pueden variar entre distribuciones.

</details>

---

## 🚀 Instalación rápida

### 1. Clonar

```bash
git clone https://github.com/fartavia3210-design/linux-desktop-containers.git
cd linux-desktop-containers
```

### 2. Verificar dependencias

```bash
docker --version
docker buildx version
xfreerdp3 /version
python3 --version
```

### 3. Construir Arch Linux + XFCE

```bash
docker buildx build \
  --load \
  --progress=plain \
  -t arch-xfce:1.0.0 \
  distros/arch/xfce
```

### 4. Abrir el administrador

```bash
chmod +x linux-desktops
./linux-desktops
```

---

## 🎮 Menú interactivo

```text
==========================================
       Linux Desktop Containers
==========================================

Selecciona una distribución:

  1) Arch Linux
  2) Debian
  3) Ubuntu
  4) Fedora
  5) Xubuntu
  6) Lubuntu

  0) Volver / Salir
```

El menú lee automáticamente:

```text
catalog.json
```

Por eso las nuevas combinaciones pueden agregarse al catálogo sin reescribir el menú principal.

---

## 🗂️ Estructura

```text
linux-desktop-containers/
│
├── catalog.json
├── linux-desktops
├── README.md
│
├── common/
│   ├── security/
│   │   └── seccomp-brave.json
│   └── scripts/
│
├── distros/
│   ├── arch/
│   │   ├── base/
│   │   ├── xfce/
│   │   ├── kde/
│   │   └── gnome/
│   ├── debian/
│   ├── ubuntu/
│   ├── fedora/
│   ├── xubuntu/
│   │   ├── base/
│   │   └── xfce/
│   └── lubuntu/
│       ├── base/
│       └── lxqt/
│
├── docs/
└── .github/
    └── workflows/
```

---

## 🔐 Seguridad

La implementación de Arch + XFCE usa:

```text
common/security/seccomp-brave.json
```

y evita depender de:

```text
seccomp=unconfined
```

Brave fue validado desde:

```text
brave://sandbox
```

con:

```text
You are adequately sandboxed.
```

XRDP se publica solo en:

```text
127.0.0.1:3389
```

> [!CAUTION]
> No expongas el puerto RDP directamente a Internet sin una capa adicional de seguridad.

### Credenciales actuales de desarrollo

```text
Usuario: arch
Contraseña: 1234
```

Son credenciales temporales y deberán convertirse en configuración segura antes de considerar el proyecto listo para uso general.

---

## 🔊 Audio

```text
Aplicación
    ↓
PipeWire
    ↓
pipewire-module-xrdp
    ↓
XRDP / rdpsnd
    ↓
FreeRDP /sound
    ↓
Audio del host
```

No es necesario montar el socket PipeWire/PulseAudio del host.

---

## 🧩 FreeRDP

La conexión actual utiliza:

```text
/dynamic-resolution
/clipboard
/sound
/cert:ignore
```

para resolución dinámica, portapapeles, audio y conexión al certificado local de XRDP durante desarrollo.

---

## 🛣️ Roadmap

- [x] Estructura multi-distro
- [x] `catalog.json`
- [x] Menú `linux-desktops`
- [x] Arch Linux + XFCE
- [x] XRDP + H.264
- [x] Audio PipeWire por RDP
- [x] Brave + sandbox
- [x] Perfil seccomp personalizado
- [ ] Arch Linux + KDE Plasma
- [ ] Arch Linux + GNOME
- [ ] Debian + XFCE / KDE / GNOME
- [ ] Ubuntu + XFCE / KDE / GNOME
- [ ] Fedora + XFCE / KDE / GNOME
- [ ] Xubuntu + XFCE
- [ ] Lubuntu + LXQt
- [ ] Imágenes preconstruidas
- [ ] GitHub Actions

---

## 🤝 Contribuciones

Las contribuciones pueden incluir nuevas combinaciones distro/escritorio, correcciones de Dockerfiles, mejoras de seguridad, compatibilidad con más hosts, mejoras del menú, documentación y pruebas.

---

## 🧪 Filosofía

Este proyecto no pretende reemplazar una VM en todos los escenarios. Busca ofrecer una forma **rápida, reproducible y práctica** de levantar escritorios Linux en Docker para pruebas, aprendizaje, desarrollo y experimentación.

---

# 🇬🇧 English

## ✨ What is this project?

**Linux Desktop Containers** is a collection of graphical Linux environments running inside Docker containers.

The goal is to select a distribution and desktop environment from a simple menu, start its container, and automatically open a graphical session through **XRDP + FreeRDP**, without creating a full virtual machine.

```text
Distribution
    ↓
Desktop environment
    ↓
Docker
    ↓
XRDP + H.264
    ↓
FreeRDP
    ↓
Linux desktop
```

Supported/planned distributions:

- Arch Linux
- Debian
- Ubuntu
- Fedora
- Xubuntu
- Lubuntu

Desktop environments currently targeted:

- XFCE
- KDE Plasma
- GNOME
- LXQt only for Lubuntu

---

## 🚦 Current status

> [!IMPORTANT]
> The project is under development. **Arch Linux + XFCE** is currently the first integrated and validated combination.

| Distribution | XFCE | KDE Plasma | GNOME | LXQt |
|---|:---:|:---:|:---:|:---:|
| Arch Linux | ✅ Available | 🕒 Planned | 🕒 Planned | — |
| Debian | 🕒 Planned | 🕒 Planned | 🕒 Planned | — |
| Ubuntu | 🕒 Planned | 🕒 Planned | 🕒 Planned | — |
| Fedora | 🕒 Planned | 🕒 Planned | 🕒 Planned | — |
| Xubuntu | 🕒 Planned | — | — | — |
| Lubuntu | — | — | — | 🕒 Planned |

---

## 📦 Requirements

| Dependency | Purpose |
|---|---|
| **Docker Engine** | Run containers |
| **Docker Buildx** | Build images |
| **FreeRDP 3** | Open graphical RDP sessions |
| **Python 3** | Run `linux-desktops` |
| **Git** | Clone and update the project |
| **Bash** | Run launchers |

The current launcher expects:

```text
xfreerdp3
```

### Arch Linux / CachyOS

```bash
sudo pacman -S --needed docker docker-buildx freerdp python git
sudo systemctl enable --now docker
```

Optional Docker access without `sudo`:

```bash
sudo usermod -aG docker "$USER"
```

> [!WARNING]
> Membership in the `docker` group grants root-level privileges over the Docker daemon.

---

## 🚀 Quick start

```bash
git clone https://github.com/fartavia3210-design/linux-desktop-containers.git
cd linux-desktop-containers
```

Build the currently available Arch + XFCE image:

```bash
docker buildx build \
  --load \
  --progress=plain \
  -t arch-xfce:1.0.0 \
  distros/arch/xfce
```

Start the manager:

```bash
chmod +x linux-desktops
./linux-desktops
```

---

## 🎮 Interactive manager

The Python manager reads `catalog.json` dynamically.

```text
Linux Desktop Containers

1) Arch Linux
2) Debian
3) Ubuntu
4) Fedora
5) Xubuntu
6) Lubuntu
0) Exit
```

New combinations can therefore be added to the catalog without hardcoding them into the main menu.

---

## 🔐 Security

The validated Arch + XFCE environment uses:

```text
common/security/seccomp-brave.json
```

instead of relying on:

```text
seccomp=unconfined
```

Brave reports:

```text
You are adequately sandboxed.
```

XRDP is bound only to:

```text
127.0.0.1:3389
```

> [!CAUTION]
> Do not expose the RDP port directly to the Internet without an additional security layer.

Current development credentials:

```text
Username: arch
Password: 1234
```

These are temporary development credentials.

---

## 🔊 Audio architecture

```text
Application
    ↓
PipeWire
    ↓
pipewire-module-xrdp
    ↓
XRDP / rdpsnd
    ↓
FreeRDP /sound
    ↓
Host audio
```

---

## 🛣️ Roadmap

- [x] Multi-distribution repository structure
- [x] `catalog.json`
- [x] `linux-desktops` manager
- [x] Arch Linux + XFCE
- [x] XRDP + H.264
- [x] RDP PipeWire audio
- [x] Brave sandbox
- [x] Custom seccomp profile
- [ ] Arch Linux + KDE Plasma
- [ ] Arch Linux + GNOME
- [ ] Debian variants
- [ ] Ubuntu variants
- [ ] Fedora variants
- [ ] Xubuntu + XFCE
- [ ] Lubuntu + LXQt
- [ ] Prebuilt images
- [ ] GitHub Actions

---

## 🤝 Contributing

Contributions are welcome: new distro/desktop combinations, Dockerfile fixes, security improvements, host compatibility, manager improvements, documentation, testing and bug reports.

---

## 🧪 Philosophy

This project is not intended to replace virtual machines in every scenario. Its goal is to provide a **fast, reproducible and practical** way to launch complete Linux desktops in Docker for testing, learning, development and experimentation.

---

<div align="center">

### 🐧 Build it. Start it. Explore Linux.

**Linux Desktop Containers**

</div>
