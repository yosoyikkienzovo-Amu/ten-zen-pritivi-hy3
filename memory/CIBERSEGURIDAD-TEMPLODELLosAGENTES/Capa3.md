## Capa 2: Cifrado Total (LUKS2 + TPM2)

### 2.1 LUKS2 Full Disk Encryption

Kicksecure ya instala LUKS2 por defecto. Pero vamos a endurecerlo.

bash

common.copy

```bash
# Verifica que usas LUKS2 (no LUKS1)
sudo cryptsetup luksDump /dev/sda3 | grep "Version:"
# Debe mostrar: Version: 2

# Verifica algoritmo de cifrado
sudo cryptsetup luksDump /dev/sda3 | grep -A 5 "Cipher:"
# Ideal: aes-xts-plain64 (512 bits key)

# Si no es LUKS2, convierte (¡riesgo de pérdida de datos!)
# sudo cryptsetup convert /dev/sda3 --type luks2
```

### 2.2 Gestión de Key Slots (Múltiples Llaves)

LUKS2 permite 8 key slots. Organízalos así:

segment.table

|Slot|Tipo|Propósito|Almacenamiento|
|:--|:--|:--|:--|
|0|Passphrase primaria|Uso diario|Tu memoria (Diceware 7+ palabras)|
|1|Passphrase recovery|Emergencia|Escrita en papel, guardada en caja fuerte física|
|2|Keyfile|Automatización|USB externo cifrado (diferente del sistema)|
|3|Keyfile backup|Recuperación|USB externo diferente, ubicación física alterna|

bash

common.copy

```bash
# Verifica slots actuales
sudo cryptsetup luksDump /dev/sda3 | grep -A 20 "Keyslots:"

# Cambia passphrase primaria (Slot 0)
sudo cryptsetup luksChangeKey --key-slot 0 /dev/sda3

# Añade passphrase recovery (Slot 1)
sudo cryptsetup luksAddKey --key-slot 1 /dev/sda3
# Usa passphrase de 10+ palabras, nunca la uses para login

# Crea keyfile seguro para Slot 2
dd if=/dev/urandom of=/media/usb-recovery/luks-keyfile bs=4096 count=1
chmod 400 /media/usb-recovery/luks-keyfile
sudo cryptsetup luksAddKey --key-slot 2 /dev/sda3 /media/usb-recovery/luks-keyfile

# Testea cada slot
sudo cryptsetup open --test-passphrase --key-slot 0 /dev/sda3
sudo cryptsetup open --test-passphrase --key-slot 1 /dev/sda3
```

### 2.3 TPM2 + Clevis: Auto-unlock Seguro

El TPM2 sella la llave de cifrado al estado del hardware. Si alguien roba el disco, no puede desencriptarlo sin tu placa base.

bash

common.copy

```bash
# Instala Clevis
sudo apt install -y clevis clevis-luks clevis-dracut clevis-systemd tpm2-tools

# Verifica TPM2
ls /dev/tpm*
cat /sys/class/tpm/tpm0/tpm_version_major

# Bind LUKS a TPM2 (PCR 7 = Secure Boot state)
sudo clevis luks bind -d /dev/sda3 tpm2 '{"pcr_ids":"7"}'
# Pide tu passphrase actual, luego sella en TPM

# Verifica binding
sudo clevis luks list -d /dev/sda3
# Output: 2: tpm2 '{"hash":"sha256","key":"ecc","pcr_bank":"sha256","pcr_ids":"7"}'

# Testea reboot
sudo reboot
# Al arrancar, el TPM debería desbloquear automáticamente
# Si falla (ej. después de BIOS update), usa passphrase manual
```

**⚠️ IMPORTANTE:** Mantén siempre una passphrase manual como fallback. Si el TPM falla (firmware update, cambio de hardware), perderás acceso sin passphrase.[](https://oneuptime.com/blog/post/2026-03-04-luks-encryption-tpm2-key-rhel-9/view)

### 2.4 Cifrado de Swap

bash

common.copy

```bash
# Verifica swap cifrada
swapon --show
# Debe mostrar /dev/mapper/cryptswap1 o similar

# Si no está cifrada, configúrala
sudo swapoff -a
sudo cryptsetup luksFormat /dev/sdaX  # tu partición swap
sudo cryptsetup open /dev/sdaX cryptswap
sudo mkswap /dev/mapper/cryptswap
sudo swapon /dev/mapper/cryptswap

# Añade a /etc/crypttab
echo "cryptswap /dev/sdaX none luks" | sudo tee -a /etc/crypttab

# Actualiza fstab
echo "/dev/mapper/cryptswap none swap sw 0 0" | sudo tee -a /etc/fstab
```

---

