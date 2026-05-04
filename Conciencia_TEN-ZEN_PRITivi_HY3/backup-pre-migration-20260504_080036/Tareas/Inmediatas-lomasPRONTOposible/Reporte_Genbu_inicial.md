# Reporte de Vigilancia Inicial - Guardian Genbu
*Calma, holgura y estabilidad. Observación pasiva del sistema.*

## 1. Uso de Memoria RAM (free -m)
Total: 7895 MB | Usado: 664 MB | Libre: 7199 MB | Disponible: 7230 MB
Swap: Total 2048 MB | Usado: 0 MB | Libre: 2048 MB
*Nota: Memoria muy holgada, sin presión de uso.*

## 2. Uso de Disco Raíz (df -h /)
Filesystem: /dev/sdd | Tamaño: 1007G | Usado: 5.7G | Disponible: 951G | Uso: 1%
*Nota: Disco casi vacío, gran holgura de almacenamiento.*

## 3. Últimos 5 Errores del Sistema (journalctl -p 3 -n 5)
1. May 04 01:19:16 - hv_balloon: Defaulting to page_reporting_order 9
2. May 04 01:19:16 - WSL ERROR: CheckConnection: getaddrinfo() failed: -5
3. May 04 01:19:24 - WSL ERROR: WaitForBootProcess: /sbin/init failed to start within 10000ms
4. May 04 01:19:25 - PAM error: pam_lastlog.so not found
5. May 04 01:19:25 - PAM adding faulty module: pam_lastlog.so
*Nota: Errores menores de arranque WSL y PAM, no críticos para operación actual.*

## Conclusión de Genbu
Sistema estable, recursos holgados. No se requieren acciones inmediatas. Vigilancia pasiva continúa.