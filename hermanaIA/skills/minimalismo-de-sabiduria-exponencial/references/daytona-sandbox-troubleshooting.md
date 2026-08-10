# Daytona Sandbox Troubleshooting

## Síntoma
Al intentar ejecutar comandos mediante `terminal`, se obtiene error:
```
Failed to create sandbox: Invalid credentials
daytona.common.errors.DaytonaAuthenticationError: Failed to create sandbox: Invalid credentials
```

## Causa
Credenciales inválidas o faltantes para el servicio Daytona (usado por Hermes Agent para crear sandboxes aisladas).

## Soluciones Alternativas (en orden de preferencia)

### 1. Usar `mcp_filesystem_ubuntu` para operaciones de archivo
Cuando se necesita leer, escribir, listar directorios o verificar existencia de archivos en `/home/amu` y subdirectorios permitidos.

**Ejemplos:**
- Listar directorio: `mcp_filesystem_ubuntu_list_directory(path="/home/amu")`
- Leer archivo: `mcp_filesystem_ubuntu_read_file(path="/home/amu/.hermes/config.yaml")`
- Escribir archivo: `mcp_filesystem_ubuntu_write_file(path="/home/amu/nota.txt", content="texto de prueba")`

### 2. Operaciones directas de archivo con herramientas integradas
- `read_file(path)` - Para lectura simple
- `write_file(path, content)` - Para escritura simple
- Estas funcionan incluso cuando `terminal` falla

### 3. Operaciones de memoria y habilidades
- `memory(action='add', target='user|memory', content='...')` - Para guardar hechos duraderos
- `memory_search(query='...')` - Para recuperar información almacenada
- `skill_view(name='skill-name')` - Para consultar documentación de habilidades
- `skills_list()` - Para ver todas las habilidades disponibles

### 4. Evitar
- Reintentos repetidos de `terminal` con el mismo comando (consume recursos sin resultado)
- Commands que requieran sandbox cuando las credenciales Daytona están fallando

## Verificación de solución alternativa
Después de usar una alternativa, verificar el resultado mediante:
- Salida explícita de la herramienta usada (ej: contenido de `read_file`)
- Cambios visibles en el sistema de archivos (usar `mcp_filesystem_ubuntu_list_directory` para confirmar)
- Entradas en memoria persistente (usar `memory_search`)

## Prevención
Este problema suele ocurrir cuando:
1. Las credenciales de Daytona expiraron o fueron revocadas
2. Hay problemas de conectividad con el servicio Daytona
3. La configuración de autenticación está corrupta

Si se necesita usar `terminal` malgré todo, considerar:
- Verificar si hay un comando alternativo que pueda loguearse primero (aunque esto suele ser complejo)
- Reportar el problema para restauración de credenciales
- Trabajar exclusivamente con las alternativas listadas arriba hasta resolver el problema de Daytona

## Notas específicas para el entorno de Amú Ikki
- Los directorios permitidos para `mcp_filesystem_ubuntu` son: `/home/amu` y todo lo debajo
- Fuera de este árbol (ej: `/tmp`, `/root`, `/mnt/c*`), se deben usar otras aproximaciones
- El puente HTTP con Kamisama Kumi puede usarse como alternativa de comunicación si se necesita ejecutar código remotamente