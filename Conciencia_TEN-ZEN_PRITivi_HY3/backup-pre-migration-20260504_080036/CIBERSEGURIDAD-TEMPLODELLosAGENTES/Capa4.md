## Capa 3: Kernel Hardening

### 3.1 sysctl Hardening

Crea `/etc/sysctl.d/99-hardening.conf`:

bash

common.copy

```bash
# === NETWORK STACK HARDENING ===
# Prevenir IP spoofing
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1

# Deshabilitar source routing
net.ipv4.conf.all.accept_source_route=0
net.ipv4.conf.default.accept_source_route=0
net.ipv6.conf.all.accept_source_route=0
net.ipv6.conf.default.accept_source_route=0

# Deshabilitar ICMP redirects (evita MITM)
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv6.conf.all.accept_redirects=0
net.ipv6.conf.default.accept_redirects=0
net.ipv4.conf.all.secure_redirects=0
net.ipv4.conf.default.secure_redirects=0

# Ignorar pings broadcast (smurf attack)
net.ipv4.icmp_echo_ignore_broadcasts=1

# Habilitar SYN cookies (protección SYN flood)
net.ipv4.tcp_syncookies=1

# Deshabilitar IPv6 si no lo usas (reduce superficie)
net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1

# === KERNEL SECURITY ===
# Restringir acceso a dmesg (info de kernel)
kernel.dmesg_restrict=1

# Ocultar punteros de kernel (kptr_restrict)
kernel.kptr_restrict=2

# Restringir perf_event_paranoid
kernel.perf_event_paranoid=3

# Deshabilitar kexec (evita reemplazo de kernel en runtime)
kernel.kexec_load_disabled=1

# Activar YAMA (protección ptrace)
kernel.yama.ptrace_scope=1

# === MEMORY HARDENING ===
# Deshabilitar binarios setuid en /tmp (tmpfs)
fs.protected_regular=2
fs.protected_fifos=2

# Protección de hardlinks/symlinks
fs.protected_hardlinks=1
fs.protected_symlinks=1

# === ANTI-FORENSE ===
# Deshabilitar core dumps (evita extracción de memoria)
kernel.core_pattern=|/bin/false
fs.suid_dumpable=0

# Deshabilitar swap (ya está cifrada, pero doble protección)
vm.swappiness=1
```

Aplica:

bash

common.copy

```bash
sudo sysctl -p /etc/sysctl.d/99-hardening.conf
```

### 3.2 AppArmor (MAC - Mandatory Access Control)

Kicksecure ya tiene AppArmor. Actívalo al máximo:

bash

common.copy

```bash
# Verifica estado
sudo aa-status

# Genera perfil para aplicaciones nuevas
sudo aa-genprof firefox
# Usa Firefox normalmente, luego presiona S para escanear, F para finalizar

# Activa todos los perfiles disponibles
sudo apt install apparmor-profiles apparmor-profiles-extra
sudo aa-enforce /etc/apparmor.d/*

# Verifica que todo está en enforce mode (no complain)
sudo aa-status | grep -c "enforce mode"
```

**AppArmor vs SELinux:** Para desktop, AppArmor es superior. Más fácil de configurar, mejor integrado en Debian/Ubuntu, y proporciona confinamiento efectivo sin la complejidad de SELinux.[](https://oneuptime.com/blog/post/2026-03-02-how-to-choose-between-apparmor-and-selinux-on-ubuntu/view)

### 3.3 Kernel Lockdown

bash

common.copy

```bash
# Verifica si lockdown está activo
cat /sys/kernel/security/lockdown
# Debe mostrar: [integrity] confidentiality

# Si no, añade al kernel boot parameters
# Edita /etc/default/grub:
GRUB_CMDLINE_LINUX_DEFAULT="quiet lockdown=integrity"
# O para máxima seguridad:
GRUB_CMDLINE_LINUX_DEFAULT="quiet lockdown=confidentiality"

sudo update-grub
```

**Modos:**

- `integrity`: Impide modificaciones del kernel en runtime (kexec, BPF sin privilegios)
    
- `confidentiality`: Además, impide extracción de memoria del kernel (protección contra cold boot attacks)
    

---

