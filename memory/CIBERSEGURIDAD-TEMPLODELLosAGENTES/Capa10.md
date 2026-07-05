## Capa 9: Hardening del Navegador

### 9.1 Firefox Hardened (Alternativa a Tor Browser)

bash

common.copy

```bash
# Instala Firefox ESR (más estable, menos cambios)
sudo apt install firefox-esr

# about:config hardening:
// Deshabilitar telemetry
browser.tabs.firefox-view=false
toolkit.telemetry.enabled=false
toolkit.telemetry.unified=false
toolkit.telemetry.archive.enabled=false
datareporting.healthreport.uploadEnabled=false
datareporting.policy.dataSubmissionEnabled=false

// Deshabilitar WebRTC leak
media.peerconnection.enabled=false

// Deshabilitar DNS over HTTPS (si usas Tor o VPN propia)
network.trr.mode=5

// Strict tracking protection
privacy.trackingprotection.enabled=true
privacy.trackingprotection.socialtracking.enabled=true

// Container tabs (aislamiento por sitio)
browser.tabs.firefox-view=false
```

### 9.2 Extensiones Esenciales

segment.table

|Extensión|Propósito|Repositorio|
|:--|:--|:--|
|**uBlock Origin**|Bloqueo de trackers/ads|`github.com/gorhill/uBlock`|
|**NoScript**|Control granular de JavaScript|`github.com/hackademix/noscript`|
|**HTTPS Everywhere**|Forzar HTTPS (o usar HTTPS-Only Mode nativo)|EFF|
|**Privacy Badger**|Heurística anti-tracking|EFF|
|**Decentraleyes**|CDN local (evita tracking por CDN)|`git.synz.io/Synzvato/decentraleyes`|

---

