# Uso de habilidades de agente con Gemini CLI

## Configuración

### Opción 1: Instalar como habilidades (recomendado)

Gemini CLI tiene un sistema de habilidades nativo que descubre automáticamente los archivos `SKILL.md` en los directorios `.gemini/skills/` o `.agents/skills/`.Cada habilidad se activa según demanda cuando coincide con tu tarea.

**Instalar desde el repositorio:**

```golpecito
Instalación de habilidades de Géminis https://github.com/addyosmani/agent-skills.git --path skills
```

**O instalar desde un clon local:**

```golpecito
clon de git https://github.com/addyosmani/agent-skills.git
instalación de habilidades de gemini /ruta/a/agent-skills/skills/
```

**Instalar solo para un espacio de trabajo específico:**

```golpecito
instalación de habilidades de gemini /ruta/a/agent-skills/skills/ --scope espacio de trabajo
```

Las habilidades instaladas en el ámbito del espacio de trabajo van a `.gemini/skills/` (o `.agents/skills/`).Las habilidades a nivel de usuario van en `~/.gemini/skills/`.

Una vez instalado, verifique con:

```
/lista de habilidades
```

Gemini CLI inyecta automáticamente nombres y descripciones de habilidades en el mensaje.Cuando reconoce una tarea coincidente, solicita permiso para activar la habilidad antes de cargar sus instrucciones completas.

### Opción 2: GEMINI.md (Contexto persistente)

Para las habilidades que desea cargar siempre como contexto persistente del proyecto (en lugar de activación bajo demanda), agréguelas al `GEMINI.md` de su proyecto:

```golpecito
# Crea GEMINI.md con habilidades básicas como contexto persistente
cat /ruta/a/habilidades-del-agente/habilidades/implementación-incremental/SKILL.md > GEMINI.md
echo -e "\n---\n" >> GÉMINIS.md
cat /ruta/hacia/habilidades-del-agente/habilidades/revisión-de-código-y-calidad/SKILL.md >> GEMINI.md
```

También puedes modularizar importando desde archivos separados:

```rebaja
# Instrucciones del proyecto

@skills/desarrollo-dirigido-por-pruebas/SKILL.md
@skills/implementación-incremental/SKILL.md
```

Utilice `/memory show` para verificar el contexto cargado y `/memory reload` para actualizar después de los cambios.

> **Habilidades vs GEMINI.md:** Las habilidades son experiencia bajo demanda que se activan solo cuando son relevantes, manteniendo limpia la ventana de contexto.GEMINI.md proporciona un contexto persistente cargado para cada mensaje.Utilice habilidades para flujos de trabajo específicos de fases y GEMINI.md para convenciones de proyectos siempre activas.

## Configuración recomendada

### Siempre activo (GEMINI.md)

Agregue estos como contexto persistente para cada sesión:

- `implementación-incremental`: construir en pequeñas porciones verificables
- `revisión-y-calidad del código`: revisión de cinco ejes

### Bajo demanda (habilidades)

Instálalas como habilidades para que se activen solo cuando sean relevantes:

- `desarrollo basado en pruebas`: se activa al implementar lógica o corregir errores
- `spec-driven-development`: se activa al iniciar un nuevo proyecto o característica
- `frontend-ui-engineering`: se activa al crear la interfaz de usuario
- `seguridad y refuerzo`: se activa durante las revisiones de seguridad
- `optimización del rendimiento`: se activa durante el trabajo de rendimiento

## Configuración avanzada

### Integración MCP

Muchas habilidades de este paquete aprovechan las herramientas del [Protocolo de contexto modelo (MCP)](https://modelcontextprotocol.io/) para interactuar con el entorno.Por ejemplo:

- `browser-testing-with-devtools` utiliza la extensión MCP `chrome-devtools`.
- La "optimización del rendimiento" puede beneficiarse de las herramientas MCP relacionadas con el rendimiento.

Para habilitarlos, asegúrese de tener las extensiones MCP relevantes instaladas en la configuración de su CLI de Gemini (`~/.gemini/config.json`).

### Ganchos de sesión

Gemini CLI admite enlaces de ciclo de vida de sesión.Puede usarlos para inyectar contexto automáticamente o ejecutar scripts de validación al inicio de una sesión.

Para replicar la experiencia de "habilidades de agente" de otras herramientas, puede configurar un enlace "SessionStart" que le recuerde las habilidades disponibles o cargue una metahabilidad.

### Carga de contexto explícito

Puedes cargar explícitamente cualquier habilidad en tu sesión actual haciendo referencia a ella con el símbolo `@` en tu mensaje:

```rebaja
Utilice la habilidad @skills/test-driven-development/SKILL.md para implementar esta solución.
```

Esto resulta útil cuando desea asegurarse de que se siga un flujo de trabajo específico sin esperar el descubrimiento automático.

## Consejos de uso

1. **Prefiera las habilidades a GEMINI.md**: las habilidades se activan a pedido y mantienen enfocada su ventana de contexto.Sólo coloca habilidades en GEMINI.md si quieres que siempre estén cargadas.
2. **Las descripciones de las habilidades importan**: cada SKILL.md tiene un campo "descripción" en su portada que indica a los agentes cuándo activarlo.Las descripciones de este repositorio están optimizadas para el descubrimiento automático en todas las herramientas compatibles (Claude Code, Gemini CLI, etc.) al indicar claramente *qué* hace la habilidad y *cuándo* debe activarse.
3. **Utilice agentes para revisión**: copie el contenido de `agents/code-reviewer.md` cuando solicite revisiones de código estructurado.
4. **Combinar con referencias**: listas de verificación de referencias de `referencias/` cuando se trabaja en áreas de calidad específicas, como pruebas o desempeño.