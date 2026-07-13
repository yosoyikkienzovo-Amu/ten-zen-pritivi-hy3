## Capa 8: Detección de Intrusos

### 8.1 rkhunter (Rootkit Hunter)

bash

common.copy

```bash
# Instala y configura
sudo apt install rkhunter

# Configura mirrors y email alerts
sudo tee /etc/rkhunter.conf.local << 'EOF'
UPDATE_MIRRORS=1
MIRRORS_MODE=0
ROTATE_MIRRORS=1
MAIL_CMD=mail -s "[rkhunter] Alerta - $(hostname)"
[email protected]
ALLOWHIDDENDIR=/dev/.udev
ALLOWHIDDENDIR=/dev/.static
ALLOWHIDDENFILE=/dev/.blkid.tab
ALLOWHIDDENFILE=/dev/.blkid.tab.old
EOF

# Actualiza base de datos
sudo rkhunter --update
sudo rkhunter --propupd

# Escaneo completo
sudo rkhunter --check --skip-keypress --report-warnings-only
```

### 8.2 chkrootkit

bash

common.copy

```bash
sudo apt install chkrootkit
sudo chkrootkit -q
```

### 8.3 USBGuard (Bloqueo de USB no autorizados)

bash

common.copy

```bash
# Instala
sudo apt install usbguard usbguard-dbus

# Genera política inicial (bloquea TODO excepto lo conectado ahora)
sudo usbguard generate-policy > /etc/usbguard/rules.conf

# Activa
sudo systemctl enable --now usbguard

# Verifica estado
sudo usbguard list-devices

# Para permitir nuevo dispositivo:
sudo usbguard allow-device <id>
```

**⚠️ IMPORTANTE:** Configura USBGuard ANTES de reiniciar, o perderás acceso a teclado/ratón.[](https://www.stigviewer.com/stigs/red_hat_enterprise_linux_8/2025-03-26/finding/V-244548)

### 8.4 AIDE (Advanced Intrusion Detection Environment)

bash

common.copy

```bash
sudo apt install aide
sudo aideinit
sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db

# Escaneo diario (añade a cron)
0 3 * * * /usr/bin/aide --check | mail -s "AIDE Check $(hostname)" root
```

---

