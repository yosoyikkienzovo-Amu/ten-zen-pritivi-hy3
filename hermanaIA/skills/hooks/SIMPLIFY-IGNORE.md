# gancho simplificar-ignorar

Protección a nivel de bloque para `/code-simplify`.Código de marca que nunca debería simplificarse: el modelo no lo verá.

## Configuración

1. Anota los bloques que deseas proteger:

```js
/* simplificar-ignorar-inicio: rendimiento crítico */
// XOR desenrollado manualmente: 3 veces más rápido que un bucle
resultado[0] = buf[0] ^ clave[0];
resultado[1] = buf[1] ^ clave[1];
resultado[2] = buf[2] ^ clave[2];
resultado[3] = buf[3] ^ clave[3];
/* simplificar-ignorar-fin */
```

2. Agregue ganchos a `.claude/settings.json`:

```json
{
"ganchos": {
"Uso previo a la herramienta": [
{
"matcher": "Leer",
"ganchos": [{ "tipo": "comando", "comando": "bash ${CLAUDE_PROJECT_DIR}/hooks/simplify-ignore.sh" }]
}
],
"Uso posterior a la herramienta": [
{
"matcher": "Editar|Escribir",
"ganchos": [{ "tipo": "comando", "comando": "bash ${CLAUDE_PROJECT_DIR}/hooks/simplify-ignore.sh" }]
}
],
"Detener": [
{
"ganchos": [{ "tipo": "comando", "comando": "bash ${CLAUDE_PROJECT_DIR}/hooks/simplify-ignore.sh" }]
}
]
}
}
```

3. Ejecute `/code-simplify`: los bloques protegidos se convierten en `/* BLOCK_de115a1d: marcadores de posición críticos para el rendimiento */`.El modelo razona sobre el código circundante sin ver la implementación protegida.

> **Nota:** El gancho almacena copias de seguridad temporales en `.claude/.simplify-ignore-cache/`.Asegúrese de que esta ruta esté en su `.gitignore`.

## Cómo funciona

Un guión, tres eventos de enlace:

|Evento |Acción |
|---|---|
|`PreToolUse Leer` |Realiza una copia de seguridad del archivo, reemplaza los bloques con marcadores de posición `BLOCK_<hash>` in situ |
|`PostToolUse Editar\|Escribir` |Expande los marcadores de posición al código real, guarda los cambios del modelo y vuelve a filtrar |
|`Parar` |Restaura todos los archivos desde la copia de seguridad cuando finaliza la sesión |

Cada bloque tiene un contenido hash (8 caracteres hexadecimales a través de `shasum`/`sha1sum`), por lo que el recorrido de ida y vuelta no es ambiguo incluso si el modelo duplica o reordena los marcadores de posición.La caché tiene un alcance de proyecto para evitar interferencias entre sesiones.

## Sintaxis de anotación

```js
/* simplificar-ignorar-iniciar */ // básico — oculta el bloque
/* simplificar-ignorar-iniciar: motivo */ // con motivo — aparece en el marcador de posición
/* simplificar-ignorar-fin */
```

Cualquier estilo de comentario funciona (`//`, `/*`, `#`, `<!--`).Se admiten varios bloques por archivo y bloques de una sola línea.Los marcadores de posición conservan la sintaxis original del comentario (por ejemplo, `# BLOCK_xxx` para Python, `<!-- BLOCK_xxx -->` para HTML).

## Recuperación de fallos

Si Claude Code falla sin activar el gancho Detener, es posible que los archivos en el disco aún tengan marcadores de posición `BLOCK_<hash>`.Para restaurar manualmente:

```golpecito
eco '{}' |ganchos bash/simplify-ignore.sh
```

Las copias de seguridad se almacenan en `.claude/.simplify-ignore-cache/` dentro del directorio de su proyecto.

## Limitaciones conocidas

- **Los bloques de una sola línea ocultan toda la línea.** Si `simplify-ignore-start` y `simplify-ignore-end` aparecen en la misma línea que otro código, toda la línea está oculta del modelo, no solo la parte anotada.Utilice líneas dedicadas para las anotaciones.
- **La detección de sufijos de comentarios cubre `*/` y `-->` únicamente.** Los motores de plantillas con cierres de comentarios no estándar (ERB `%>`, Blade `--}}`) pueden producir marcadores de posición desequilibrados.Utilice comentarios de estilo `#` o `//` en su lugar.
- **La expansión alternativa es progresiva, no exacta.** Si el modelo altera el formato de un marcador de posición (por ejemplo, cambia el texto del motivo), el gancho intenta coincidencias progresivamente más simples: marcador de posición completo → prefijo+almohadilla+sufijo → solo hash.La alternativa de solo hash puede dejar restos cosméticos (por ejemplo, `:` o texto de motivo perdidos).Cuando esto sucede, se imprime una advertencia en stderr.
- **El cambio de nombre de archivos deja marcadores de posición.** Si el modelo cambia el nombre o mueve un archivo mediante un comando de shell, el nuevo archivo conservará los marcadores de posición `BLOCK_<hash>`.El código original se guarda como `<nombre de archivo antiguo>.recovery` cuando se detiene la sesión.Debe restaurar manualmente el código recuperado en el nuevo archivo.

## Requisitos

- `jq`, `shasum` o `sha1sum` (detectado automáticamente), Bash 3.2+