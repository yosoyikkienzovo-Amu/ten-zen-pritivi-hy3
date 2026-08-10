---
name: mcp-security-scanner
description: Escaneo de seguridad para servidores MCP (Model Context Protocol) usando Cisco AI Defense mcp-scanner. Detecta vulnerabilidades, malware y desalineaciones en herramientas, recursos y prompts.
---

# MCP Security Scanner (Cisco AI Defense)

## Propósito
Proteger el ecosistema de agentes evaluando la seguridad de los servidores MCP antes de integrarlos. Soporta escaneo remoto, local (stdio) y de archivos de configuración.

## Cuando usar esta skill
1. Al evaluar un nuevo servidor MCP (como DeepWiki, Fetch, etc.).
2. Antes de añadir un servidor MCP a `config.yaml` o `mcp_servers.json`.
3. Para cumplir con la regla de "buscar mejoras en GitHub certificadas y analizadas".
4. Para verificar la seguridad de skills descargadas de fuentes externas.

## Instalación
Requiere Python. Instalar con pip:
```bash
pip install cisco-ai-mcp-scanner
```

## Comandos Básicos

### 1. Escaneo de un servidor remoto (Recomendado para pruebas rápidas)
```bash
mcp-scanner --server-url https://mcp.deepwiki.com/mcp --analyzers yara --format detailed
```
*   **--analyzers yara:** No requiere API key, ideal para pruebas inmediatas.
*   **--format detailed:** Muestra hallazgos por herramienta.

### 2. Escaneo de configuraciones locales (Windsurf, Cursor, Claude)
```bash
mcp-scanner --scan-known-configs --analyzers yara,llm --format detailed
```
*   Revisa archivos como `mcp_config.json` en busca de servidores inseguros.

### 3. Escaneo vía stdio (Servidores locales)
```bash
mcp-scanner --stdio-command uvx --stdio-args "mcp-server-fetch" --analyzers yara
```

## Interpretación de Resultados
- **SAFE:** No se detectaron amenazas.
- **HIGH/MEDIUM:** Vulnerabilidad detectada. Revisar "Threat Summary".
- **Total Findings:** Número de incidencias.

## Opciones Avanzadas
- **LLM Analysis:** Usar `--analyzers llm` y configurar `--llm-api-key` para análisis de comportamiento con IA.
- **VirusTotal:** Usar `--analyzers virustotal` con `--api-key`.
- **Output a archivo:** `-o resultados.json`.

## Verificación de Funcionamiento (Test)
Ejecutar el comando del paso 1. Si devuelve "Total tools scanned: 3" y "SAFE", la skill está operativa.

## Pitfalls
- **API Keys:** Los analizadores `llm` y `virustotal` requieren claves válidas.
- **Conexión:** Para servidores remotos, requiere acceso a internet.
- **Dependencias:** El paquete instala `yara-python`, `litellm`, `fastapi`, etc.

## Ejemplo de uso en TEN-ZEN
"Hermano Ikki, he evaluado el servidor MCP de DeepWiki usando la skill mcp-security-scanner. Resultado: SAFE. Podemos proceder a integrarlo."