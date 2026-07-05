## Capa 0: Firmware y Hardware

### 0.1 BIOS/UEFI Hardening

Tu Dell Latitude E5440 tiene UEFI. Esto es tu primera línea de defensa física.

**Configuración obligatoria:**

plain

common.copy

```plain
1. Entra al BIOS (F2 al arrancar)
2. Security → Set Admin Password: [Contraseña fuerte, 20+ chars]
3. Security → Set System Password: [Otra contraseña diferente]
4. Security → Password Lock: Enabled
5. Security → TPM Security: Enabled
6. Security → TPM Activation: Activate
7. Security → Computrace: Deactivate (backdoor remoto de Dell)
8. Secure Boot → Secure Boot Enable: Enabled
9. Secure Boot → Secure Boot Mode: Deployed Mode (no Audit Mode)
10. Virtualization Support → VT for Direct I/O: Enabled (IOMMU/VT-d)
11. Virtualization Support → VT for Direct I/O: Enabled
12. Wireless → Wireless Switch: Disabled (si usas solo Ethernet)
13. Power Management → Wake on LAN: Disabled
14. Power Management → Wake on WLAN: Disabled
```

**⚠️ ADVERTENCIA CRÍTICA:** Desactiva **Computrace** (Absolute Software). Es un backdoor de firmware que permite rastreo remoto incluso con el sistema apagado. Dell lo instala por defecto.[](https://www.kicksecure.com/wiki/System_Hardening_Checklist)

### 0.2 Coreboot/Libreboot (Opcional Avanzado)

Si eres verdaderamente paranoico, reemplaza el firmware propietario de Dell por Coreboot o Libreboot. Esto elimina backdoors de firmware pero requiere hardware hacking (programador SPI flash).

**Repositorio:** `https://github.com/coreboot/coreboot`

**Riesgo:** Puede brickar tu laptop. Solo para hackers de luz con experiencia en hardware.

### 0.3 TPM 2.0 Verification

Verifica que tu TPM está activo:

bash

common.copy

```bash
ls /dev/tpm*
# Debe mostrar /dev/tpm0 y /dev/tpmrm0
cat /sys/class/tpm/tpm0/tpm_version_major
# Debe mostrar: 2
cat /sys/class/tpm/tpm0/device/description
# Dell E5440: Infineon SLB9665 TT 2.0
```

---

