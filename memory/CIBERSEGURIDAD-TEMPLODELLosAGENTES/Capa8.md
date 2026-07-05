## Capa 7: Gestión de Secretos

### 7.1 KeePassXC (Gestor de Contraseñas Offline)

bash

common.copy

```bash
# Instala
sudo apt install keepassxc

# Configuración recomendada:
# - Database: AES-256 + Argon2id (memory-hard KDF)
# - Key file: Sí (archivo adicional aparte de passphrase)
# - YubiKey: Si tienes, configura challenge-response
# - Auto-type: Global para login rápido y seguro
# - Browser integration: Desactivado (reduce superficie de ataque)
```

**Diceware para passphrase maestra:**

bash

common.copy

```bash
# Genera passphrase de 7 palabras (80+ bits de entropía)
sudo apt install diceware
diceware -n 7 -d " "
# Ejemplo: "correct horse battery staple xkcd comic dice"
```

### 7.2 GnuPG para Cifrado de Archivos

bash

common.copy

```bash
# Genera par de claves (RSA 4096 o Ed25519)
gpg --full-generate-key

# Cifra archivo para ti mismo
gpg --encrypt --recipient tu@email.com archivo-secreto.txt
# Genera archivo-secreto.txt.gpg

# Cifra con passphrase simétrica (para backups)
gpg --symmetric --cipher-algo AES256 archivo-backup.tar

# Firma digital
gpg --sign --armor documento-importante.pdf
```

---

