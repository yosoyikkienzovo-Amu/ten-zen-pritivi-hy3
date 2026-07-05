## Capa 6: Anonimato

### 6.1 Tor Browser (Navegación Anónima)

bash

common.copy

```bash
# Instala Tor Browser Launcher
sudo apt install torbrowser-launcher

# Descarga y verifica firma
torbrowser-launcher

# Lanza Tor Browser
torbrowser &
```

### 6.2 Hardening de Tor Browser

Configuración `about:config` para máxima seguridad (solo sitios sin JS):[](https://www.reddit.com/r/TOR/comments/1iesj87/hardened_aboutconfig_settings_for_tor_browser/)

JavaScript

common.copy

```javascript
// Nivel de seguridad: Safest
browser.security_level.security_slider;1

// Deshabilitar JavaScript (máxima seguridad, menos funcionalidad)
javascript.enabled;false

// Deshabilitar WebGL (fingerprinting vector)
webgl.disabled;true

// Deshabilitar fuentes descargables (fingerprinting)
gfx.downloadable_fonts.enabled;false

// Spoofing de User Agent
privacy.resistFingerprinting.spoofOsInUserAgentHeader;true

// Anti-tracking
privacy.trackingprotection.enabled;true
privacy.trackingprotection.fingerprinting.enabled;true
privacy.trackingprotection.cryptomining.enabled;true

// Deshabilitar geolocalización
permissions.default.geo;2

// Deshabilitar cámara/micrófono
permissions.default.camera;2
permissions.default.microphone;2

// Deshabilitar WebRTC (leak de IP real)
media.peerconnection.enabled;false
```

### 6.3 MAC Spoofing

bash

common.copy

```bash
# Instala macchanger
sudo apt install macchanger

# Spoofea MAC en cada boot
sudo nano /etc/NetworkManager/dispatcher.d/99-mac-spoof
```

bash

common.copy

```bash
#!/bin/bash
# /etc/NetworkManager/dispatcher.d/99-mac-spoof
IFACE="$1"
STATUS="$2"

if [ "$STATUS" = "up" ]; then
    # Genera MAC aleatoria
    macchanger -r "$IFACE"
fi
```

bash

common.copy

```bash
chmod +x /etc/NetworkManager/dispatcher.d/99-mac-spoof
```

### 6.4 WireGuard + Mullvad (VPN Confiable)

Mullvad es el estándar de oro en privacidad: no requiere email, acepta efectivo, código auditado.[](https://www.kunalganglani.com/blog/mozilla-vpn-wireguard-technical-review)

bash

common.copy

```bash
# Instala WireGuard
sudo apt install wireguard-tools

# Descarga config de Mullvad (cuenta anónima)
# https://mullvad.net/account/create/

# Copia config
sudo cp mullvad.conf /etc/wireguard/

# Activa
sudo wg-quick up mullvad

# Verifica (debe mostrar IP de Mullvad, no tu ISP)
curl https://am.i.mullvad.net/connected

# Para máxima seguridad: Tor sobre VPN
# Primero VPN, luego Tor Browser
# Esto oculta que usas Tor a tu ISP
```

---

