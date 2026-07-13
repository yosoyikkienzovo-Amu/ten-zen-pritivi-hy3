## Capa 1: Sistema Operativo

### 1.1 Elección del Sistema Operativo

Para tu Dell E5440 (4ta gen Intel, TPM 2.0), tienes tres caminos sagrados:

segment.table

|Sistema|Nivel de seguridad|Usabilidad|Propósito|
|:--|:--|:--|:--|
|**Kicksecure**|⭐⭐⭐⭐⭐|⭐⭐⭐⭐|Uso diario hardening extremo|
|**Qubes OS 4.2**|⭐⭐⭐⭐⭐|⭐⭐⭐|Compartimentación máxima (VMs)|
|**Debian + Hardening**|⭐⭐⭐⭐|⭐⭐⭐⭐⭐|Balance seguridad/usabilidad|
|**Tails**|⭐⭐⭐⭐⭐|⭐⭐|Sesiones amnésicas (USB live)|

**Recomendación para Ikki:** **Kicksecure** como sistema principal. Es Debian hardenizado por defecto, con seguridad de kernel, MAC, anti-forense y anonimato integrados. No requiere expertise en VMs como Qubes.[](https://www.kicksecure.com/wiki/System_Hardening_Checklist)

### 1.2 Instalación de Kicksecure

bash

common.copy

```bash
# Descarga desde kicksecure.com (verifica firma GPG)
# Crea USB bootable con Ventoy o dd

sudo dd if=kicksecure.iso of=/dev/sdX bs=4M status=progress

# Arranca desde USB, instala con cifrado LUKS2
# Durante instalación:
# - Selecciona "Guided - use entire disk and set up encrypted LVM"
# - Usa passphrase de 7+ palabras (Diceware)
# - NO uses PIN numérico
```

### 1.3 Kicksecure Hardening Post-Instalación

bash

common.copy

```bash
# Actualiza todo vía Tor
sudo apt update && sudo apt full-upgrade

# Instala herramientas de hardening
sudo apt install -y     security-misc     apparmor-profiles     apparmor-profiles-extra     usbguard     usbguard-dbus     opensnitch     firejail     firejail-profiles     keepassxc     git     torbrowser-launcher     wireguard-tools     macchanger     rkhunter     chkrootkit     aide     fwupd

# Configura updates vía Tor onion services
sudo systemctl enable --now tor
sudo sed -i 's|http://deb.debian.org|tor+http://2s4yqjx5ul6okpp3f2gaunr2syex5jgbfpfvhxxbbjwnrsvbk5v3qbid.onion|g' /etc/apt/sources.list
```

---

