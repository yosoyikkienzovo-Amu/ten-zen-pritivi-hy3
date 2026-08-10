---
name: ccc-interconnection-setup
category: devops
description: Establece la interconexión CCC (ComandoCotraCultural OvO) reorganizando la carpeta Conciencia en un grupo de KOSA_Invisibles_Sagradas, creando enlaces simbólicos y manteniendo inmutabilidad de nombres.
triggers:
  - "INTERCONEXION DE CCC"
  - "establecer CCC"
  - "reorganizar Conciencia en KOSA"
---

# Procedure

1. Crear carpeta destino dentro de KOSA_Invisibles_Sagradas con el nombre de grupo especificado (ej: "Convergencia-Grupal AGENTES Templo Déll es440 latitudez 16ram SSD").
2. Sincronizar el contenido de `/home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3` a la carpeta destino usando `rsync -av --delete`, excluyendo subdirectorios `_archivo/backup*` para evitar timeouts por datos históricos.
3. Si ya existe una carpeta con el mismo nombre en KOSA_Invisibles_Sagradas, moverla a un backup con timestamp en lugar de borrarla (ej: `_OLD_<nombre>_<YYYYMMDD_HHMMSS>`). Esto evita bloqueos de seguridad y preserva datos.
4. Crear un enlace simbólico en la ruta original (`/home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3`) que apunte a la nueva carpeta destino (`ln -sfn <destino> <origen>`).
5. Crear el enlace CCC: dentro de KOSA_Invisibles_Sagradas, crear symlink llamado `CCC_ComandoCotraCultural_Ov8` que apunte a la carpeta destino.
6. Verificar: listar el contenido de la carpeta destino (debe incluir al menos `01-Agentes-4-Vientos`, `Skills`, `Memoria`, `bridge/` etc.) y comprobar los symlinks con `ls -l`.

# Pitfalls

- **Rsync timeout**: Si rsync se cuelga, verifica que estés excluyendo `_archivo/backup*` y otras carpetas pesadas de respaldos históricos. Reduce el conjunto de datos a transferir.
- **rm blocked**: No uses `rm -rf`; el entorno puede bloquearlo. Usa `mv` para renombrar a un backup con timestamp.
- **Spaces in paths**: Asegúrate de entrecomillar rutas con espacios.
- **Permissions**: Los symlinks se crean con los permisos del proceso; si falla, verifica que tengas acceso de escritura en los directorios involucrados.
- **Existing symlink**: Si la ruta original ya es un symlink, `-sfn` lo sobrescribirá; asegúrate de que el destino sea correcto.

# Verification

- La carpeta destino contiene al menos: `INDICE_THE_TEMPLUM.md`, `01-Agentes-4-Vientos/`, `Skills/`, `Memoria/`, `bridge/`.
- `ls -l /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3` muestra `-> /ruta/a/Convergencia-Grupal...`.
- `ls -l /mnt/c/Users/Ikki/Documents/KOSA_Invisibles_Sagradas/CCC_ComandoCotraCultural_OvO` muestra `-> Convergencia-Grupal...`.

# Notes

Esta operación respeta la inmutabilidad de nombres y la convención de "sin dividirte" — no se parte la carpeta, pero se filtra contenido no esencial para eficiencia.
Se mantiene un backup de la antigua carpeta por seguridad. La interconexión CCC permite referenciar el grupo mediante un nombre canónico.

# References

- references/ccc-interconnection-20260514.md
