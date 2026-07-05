## Capa 5: Sandbox (Firejail)

### 5.1 Uso Básico

Firejail usa Linux namespaces, seccomp-bpf y capabilities para aislar aplicaciones.[](https://lobehub.com/skills/faahim-openclaw-skills-firejail-sandbox)

bash

common.copy

```bash
# Firefox aislado (sin acceso a ~/.ssh, ~/.gnupg)
firejail --blacklist=~/.ssh --blacklist=~/.gnupg --blacklist=~/Documents firefox

# Aplicación sin red (air-gapped)
firejail --net=none --private libreoffice documento-secreto.odt

# Script descargado, ejecución segura
firejail --net=none --private --read-only=/ bash script-sospechoso.sh

# Navegador con home temporal (borrado al salir)
firejail --private firefox
```

### 5.2 Perfiles Personalizados

bash

common.copy

```bash
# Genera perfil para aplicación
firejail --build=myapp.profile myapp

# Edita perfil generado
nano ~/.config/firejail/myapp.local

# Ejemplo de perfil restrictivo:
cat > ~/.config/firejail/thunderbird.local << 'EOF'
# Thunderbird: solo email, sin acceso a documentos
blacklist ${HOME}/Documents
blacklist ${HOME}/Pictures
blacklist ${HOME}/.ssh
blacklist ${HOME}/.gnupg
netfilter
nosound
private-tmp
EOF
```

### 5.3 Integración con AppArmor

bash

common.copy

```bash
# Firejail + AppArmor = doble confinamiento
firejail --apparmor firefox

# Verifica que AppArmor está activo para Firejail
sudo aa-status | grep firejail
```

---

