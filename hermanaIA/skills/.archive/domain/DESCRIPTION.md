---
nombre: dominio-intel
Descripción: Reconocimiento pasivo de dominio utilizando Python stdlib.Utilice esta habilidad para el descubrimiento de subdominios, inspección de certificados SSL, búsquedas de WHOIS, registros DNS, comprobaciones de disponibilidad de dominios y análisis masivos de múltiples dominios.No se requieren claves API.Activadores de solicitudes como "buscar subdominios", "verificar certificado SSL", "búsqueda de whois", "está disponible este dominio", "verificar estos dominios en masa".
licencia: MIT
---

Inteligencia de dominio pasiva que utiliza únicamente Python stdlib y fuentes de datos públicas.
Cero dependencias.Cero claves API.Funciona desde el primer momento.

## Capacidades

- Descubrimiento de subdominios a través de registros de transparencia de certificados crt.sh
- Inspección de certificados SSL/TLS en vivo (caducidad, cifrado, SAN, versión TLS)
- Búsqueda de WHOIS: admite más de 100 TLD mediante consultas TCP directas
- Registros DNS: A, AAAA, MX, NS, TXT, CNAME
- Verificación de disponibilidad de dominio (señales DNS + WHOIS + SSL)
- Análisis masivo multidominio en paralelo (hasta 20 dominios)

## Fuentes de datos

- crt.sh: registros de transparencia de certificados
- Servidores WHOIS: TCP directo a más de 100 servidores TLD autorizados
- Google DNS sobre HTTPS: resolución MX/NS/TXT/CNAME
- DNS del sistema: registros A/AAAA