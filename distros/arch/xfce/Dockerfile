# syntax=docker/dockerfile:1

# ============================================================
# Arch Linux + XFCE + XRDP + H.264 + Brave + PipeWire Audio
# ============================================================


# ------------------------------------------------------------
# 1. BUILDER: XRDP + XORGXRDP
# ------------------------------------------------------------
FROM archlinux:latest AS xrdp-builder

ARG XRDP_VERSION=v0.10.6.1
ARG XORGXRDP_VERSION=v0.10.5

RUN pacman -Syu --noconfirm && \
    pacman -S --needed --noconfirm \
        base-devel \
        git \
        openssl \
        pam \
        libx11 \
        libxfixes \
        libxrandr \
        libxfont2 \
        fuse3 \
        pixman \
        x264 \
        nasm \
        xorg-server-devel

WORKDIR /usr/local/src


# ----- XRDP -----

RUN git clone \
        --branch "${XRDP_VERSION}" \
        --depth 1 \
        https://github.com/neutrinolabs/xrdp.git && \
    cd xrdp && \
    git submodule update --init --recursive && \
    ./bootstrap && \
    ./configure \
        --prefix=/usr \
	--sbindir=/usr/bin \
        --sysconfdir=/etc \
        --localstatedir=/var \
        --enable-fuse \
        --enable-pixman \
        --enable-x264 && \
    make -j"$(nproc)" && \
    make install && \
    make DESTDIR=/out/xrdp install


# ----- xorgxrdp -----

RUN git clone \
        --branch "${XORGXRDP_VERSION}" \
        --depth 1 \
        https://github.com/neutrinolabs/xorgxrdp.git && \
    cd xorgxrdp && \
    ./bootstrap && \
    ./configure && \
    make -j"$(nproc)" && \
    make install && \
    make DESTDIR=/out/xorgxrdp install



# ------------------------------------------------------------
# 2. BUILDER: PIPEWIRE MODULE XRDP
# ------------------------------------------------------------
FROM archlinux:latest AS audio-builder

ARG PIPEWIRE_XRDP_COMMIT=a6e268b

RUN pacman -Syu --noconfirm && \
    pacman -S --needed --noconfirm \
        base-devel \
        git \
        pipewire \
        pipewire-audio

WORKDIR /usr/local/src

RUN git clone \
        https://github.com/neutrinolabs/pipewire-module-xrdp.git && \
    cd pipewire-module-xrdp && \
    git checkout "${PIPEWIRE_XRDP_COMMIT}" && \
    ./bootstrap && \
    ./configure && \
    make -j"$(nproc)" && \
    make DESTDIR=/out/pipewire-xrdp install



# ------------------------------------------------------------
# 3. BUILDER: BRAVE
# ------------------------------------------------------------
FROM archlinux:latest AS brave-builder

RUN pacman -Syu --noconfirm && \
    pacman -S --needed --noconfirm \
        base-devel \
        git \
        alsa-lib \
        gtk3 \
        libxss \
        nss \
        noto-fonts

RUN useradd -m -s /bin/bash builder

USER builder
WORKDIR /home/builder

RUN git clone https://aur.archlinux.org/brave-bin.git && \
    cd brave-bin && \
    makepkg --noconfirm

USER root

RUN mkdir -p /out/brave && \
    cp /home/builder/brave-bin/*.pkg.tar.zst /out/brave/



# ------------------------------------------------------------
# 4. IMAGEN FINAL
# ------------------------------------------------------------
FROM archlinux:latest

ENV ARCH_USER=arch
ENV XDG_SESSION_TYPE=x11
ENV XDG_CURRENT_DESKTOP=XFCE
ENV DESKTOP_SESSION=xfce


# Actualización completa de Arch.
# Nada de partial upgrades.
RUN pacman -Syu --noconfirm && \
    pacman -S --needed --noconfirm \
        xfce4 \
        xorg-server \
        xorg-xinit \
        xorg-xrandr \
        dbus \
        sudo \
        openssl \
        pam \
        libx11 \
        libxfixes \
        libxrandr \
        fuse3 \
        pixman \
        x264 \
        pipewire \
        pipewire-audio \
        pipewire-pulse \
        wireplumber \
        xdg-utils \
        noto-fonts \
        ca-certificates && \
    pacman -Scc --noconfirm


# ------------------------------------------------------------
# Instalar XRDP compilado
# ------------------------------------------------------------

COPY --from=xrdp-builder /out/xrdp/ /
COPY --from=xrdp-builder /out/xorgxrdp/ /


# ------------------------------------------------------------
# Instalar PipeWire XRDP
# ------------------------------------------------------------

COPY --from=audio-builder /out/pipewire-xrdp/ /


# ------------------------------------------------------------
# Instalar Brave
# ------------------------------------------------------------

COPY --from=brave-builder /out/brave/ /tmp/brave/

RUN pacman -U --noconfirm /tmp/brave/*.pkg.tar.zst && \
    rm -rf /tmp/brave


# ------------------------------------------------------------
# Usuario gráfico
# ------------------------------------------------------------

RUN useradd \
        -m \
        -G wheel \
        -s /bin/bash \
        "${ARCH_USER}" && \
    echo "${ARCH_USER}:1234" | chpasswd && \
    printf '%%wheel ALL=(ALL:ALL) ALL\n' > /etc/sudoers.d/wheel && \
    chmod 440 /etc/sudoers.d/wheel


# ------------------------------------------------------------
# Configuración XRDP / Arch
# ------------------------------------------------------------

# Arch usa /usr/lib/Xorg.
RUN sed -i \
    's|^param=Xorg$|param=/usr/lib/Xorg|' \
    /etc/xrdp/sesman.ini


# ------------------------------------------------------------
# Scripts del proyecto
# ------------------------------------------------------------

COPY startwm.sh /etc/xrdp/startwm.sh
COPY start-xfce-xrdp /usr/local/bin/start-xfce-xrdp
COPY start.sh /usr/local/bin/start.sh

RUN chmod +x \
        /etc/xrdp/startwm.sh \
        /usr/local/bin/start-xfce-xrdp \
        /usr/local/bin/start.sh


# ------------------------------------------------------------
# Directorios runtime
# ------------------------------------------------------------

RUN mkdir -p \
        /run/dbus \
        /run/user/1000 \
        /var/run/xrdp && \
    chown "${ARCH_USER}:${ARCH_USER}" /run/user/1000 && \
    chmod 700 /run/user/1000


# RDP
EXPOSE 3389


# El contenedor arranca D-Bus + sesman + XRDP automáticamente
ENTRYPOINT ["/usr/local/bin/start.sh"]
