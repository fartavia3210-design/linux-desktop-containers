FROM fedora:44

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

ENV RDP_USER=fedora

# ============================================================
# Fedora + XFCE + Xorg + XRDP
# ============================================================

RUN dnf -y upgrade --refresh && \
    dnf -y install \
        xfce4-session \
        xfce4-panel \
        xfce4-settings \
        xfce4-terminal \
        xfdesktop \
        xfwm4 \
        Thunar \
        xfce4-appfinder \
        xorg-x11-server-Xorg \
        xrdp \
        xorgxrdp \
        dbus \
        dbus-x11 \
        sudo \
        shadow-utils \
        procps-ng \
        which \
        findutils \
        iproute \
        ca-certificates \
        pipewire \
        pipewire-pulseaudio \
        wireplumber \
        pipewire-utils \
        pulseaudio-utils \
        git \
        gcc \
        make \
        autoconf \
        automake \
        libtool \
        pkgconfig \
        pipewire-devel \
        dnf-plugins-core && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# ============================================================
# PipeWire XRDP
# ============================================================

WORKDIR /tmp

RUN git clone \
        https://github.com/neutrinolabs/pipewire-module-xrdp.git \
        /tmp/pipewire-module-xrdp && \
    cd /tmp/pipewire-module-xrdp && \
    ./bootstrap && \
    ./configure && \
    make -j"$(nproc)" && \
    make install && \
    rm -rf /tmp/pipewire-module-xrdp

# ============================================================
# Brave Browser
# ============================================================

RUN dnf config-manager addrepo \
        --from-repofile=https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo && \
    dnf -y install brave-browser && \
    dnf clean all && \
    rm -rf /var/cache/dnf

# ============================================================
# Usuario gráfico
# ============================================================

RUN useradd \
        -m \
        -G wheel \
        -s /bin/bash \
        "${RDP_USER}" && \
    echo "${RDP_USER}:1234" | chpasswd

# ============================================================
# Desactivar XFCE PolicyKit Agent en XRDP
# ============================================================

RUN mkdir -p /home/fedora/.config/autostart && \
    printf '%s\n' \
        '[Desktop Entry]' \
        'Type=Application' \
        'Name=XFCE PolKit' \
        'Hidden=true' \
        > /home/fedora/.config/autostart/xfce-polkit.desktop && \
    chown -R fedora:fedora /home/fedora/.config

# ============================================================
# Sesión XFCE específica para XRDP
# ============================================================

COPY start-xfce-xrdp /usr/local/bin/start-xfce-xrdp

RUN chmod +x /usr/local/bin/start-xfce-xrdp && \
    sed -i \
        's|^EnableUserWindowManager=.*|EnableUserWindowManager=false|' \
        /etc/xrdp/sesman.ini && \
    sed -i \
        's|^DefaultWindowManager=.*|DefaultWindowManager=/usr/local/bin/start-xfce-xrdp|' \
        /etc/xrdp/sesman.ini

# ============================================================
# Arranque del contenedor
# ============================================================

COPY start.sh /usr/local/bin/start-rdp

RUN chmod +x /usr/local/bin/start-rdp

WORKDIR /

EXPOSE 3389

CMD ["/usr/local/bin/start-rdp"]
