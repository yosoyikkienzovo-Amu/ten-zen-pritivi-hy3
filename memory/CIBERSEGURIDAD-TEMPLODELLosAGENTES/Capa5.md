## Capa 4: Firewall de Aplicaciones (OpenSnitch)

### 4.1 Instalación y Configuración

OpenSnitch es el "Little Snitch" de Linux. Intercepta conexiones salientes a nivel de aplicación.[](https://www.kunalganglani.com/blog/littlesnitch-linux-opensnitch-review)

bash

common.copy

```bash
# Instala (ya instalado en paso 1.3, pero verifica)
sudo apt install -y opensnitch python3-opensnitch-ui

# Activa servicio
sudo systemctl enable --now opensnitchd

# Inicia GUI
opensnitch-ui &
```

### 4.2 Configuración de Reglas Iniciales

**Reglas base (bloqueo por defecto, permitir lo esencial):**

yaml

common.copy

```yaml
# ~/.config/opensnitch/rules/system-updates.yaml
name: system-updates
enabled: true
precedence: true
action: allow
duration: always
operator:
  type: simple
  operand: process.path
  data: /usr/bin/apt

# ~/.config/opensnitch/rules/tor-traffic.yaml
name: tor-traffic
enabled: true
precedence: true
action: allow
duration: always
operator:
  type: simple
  operand: process.path
  data: /usr/bin/tor

# ~/.config/opensnitch/rules/block-all.yaml (default deny)
name: block-all
enabled: true
precedence: false
action: deny
duration: always
operator:
  type: simple
  operand: process.path
  data: .*
```

### 4.3 Backend eBPF (Recomendado)

El backend eBPF es superior a NFQueue. No conflictúa con iptables, menor latencia, compatible con containers.[](https://www.kunalganglani.com/blog/littlesnitch-linux-opensnitch-review)

bash

common.copy

```bash
# Verifica que usas eBPF
sudo cat /etc/opensnitchd/default-config.json | grep "Backend"
# Debe mostrar: "Backend": "ebpf"

# Si no, edita:
sudo nano /etc/opensnitchd/default-config.json
# Cambia "Backend" de "nfqueue" a "ebpf"

# Reinicia
sudo systemctl restart opensnitchd
```

---

