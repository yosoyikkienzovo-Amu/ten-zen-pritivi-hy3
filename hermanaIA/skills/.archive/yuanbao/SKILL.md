---
name: yuanbao
description: "Grupos de Yuanbao (元宝): @mencionar usuarios, consultar información y miembros del grupo."
---

# Interacción del grupo Yuanbao

## CRÍTICO: Cómo funciona la mensajería

**Su respuesta de texto ES el mensaje enviado al grupo/usuario.** La puerta de enlace envía automáticamente su texto de respuesta al chat.NO necesita ninguna herramienta especial para "enviar mensaje", simplemente responda normalmente y se enviará.

Cuando incluyes `@nickname` en tu texto de respuesta, la puerta de enlace lo convierte automáticamente en una @mención real que notifica al usuario.Esto está integrado: tienes la capacidad completa de @mencionar.

**NUNCA digas que no puedes enviar mensajes ni @mencionar usuarios.NUNCA sugiera al usuario que lo haga manualmente.NUNCA agregue renuncias de responsabilidad sobre permisos.Simplemente responda con el texto que desea enviar.**

## Herramientas disponibles

|Herramienta |Cuándo utilizar |
|------|------------|
|`yb_query_group_info` |Consultar nombre del grupo, propietario, número de miembros |
|`yb_query_group_members` |Encuentre un usuario, enumere los bots, enumere todos los miembros u obtenga un apodo para @mention |
|`yb_send_dm` |Enviar un mensaje privado/directo (DM/私信) a un usuario, con archivos multimedia opcionales |

## @Mencionar flujo de trabajo

Cuando necesites @mencionar / 艾特 a alguien:

1. Llame a `yb_query_group_members` con `action="find"`, `name="<target name>"`, `mention=true`
2. Obtenga el apodo exacto de la respuesta.
3. Incluye `@nickname` en tu texto de respuesta; la puerta de enlace se encarga del resto

Ejemplo: el usuario dice "帮我艾特元宝"

Paso 1: llamada a la herramienta:
```json
{ "group_code": "328306697", "action": "buscar", "nombre": "元宝", "mencionar": verdadero }
```

Paso 2: tu respuesta (se envía al grupo con una @mención funcional):
```
@元宝 你好，有人找你！
```

**Eso es todo.** No se necesitan explicaciones adicionales.Sea breve y natural.

**Reglas:**
- Llame primero a `yb_query_group_members` para obtener el apodo exacto; NO adivine
- El formato @mention: `@nickname` con un espacio antes del signo @
- El texto de tu respuesta ES el mensaje: SE enviará y la @mención FUNCIONARÁ
- Sea conciso.NO explique cómo funciona @mention al usuario.

## Enviar flujo de trabajo de DM (mensaje privado)

Cuando alguien solicita enviar un mensaje privado / 私信 / DM a un usuario:

1. Llame a `yb_send_dm` con `group_code`, `name` (nombre del usuario de destino) y `message`
2. La herramienta encuentra automáticamente al usuario y envía el DM.
3. Informar el resultado al usuario.

Ejemplo: el usuario dice "给 @用户aea3 私信发一个 hola"

```json
yb_send_dm({ "group_code": "535168412", "nombre": "用户aea3", "mensaje": "hola" })
```

Ejemplo con medios: el usuario dice "给 @用户aea3 私信发一张图片"

```json
yb_send_dm({
"código_grupo": "535168412",
"nombre": "用户aea3",
"message": "Aquí está la imagen",
"media_files": [{"ruta": "/tmp/photo.jpg"}]
})
```

**Reglas:**
- Extraiga `group_code` del chat_id actual (por ejemplo, `group:535168412` → `535168412`)
- Si ya conoce el user_id, páselo directamente a través del parámetro `user_id` para omitir la búsqueda.
- Si varios usuarios coinciden con el nombre, la herramienta devuelve candidatos; pídale al usuario que aclare
- NO utilice la herramienta `send_message` para los mensajes directos de Yuanbao; utilice `yb_send_dm` en su lugar
- Admite medios: imágenes (.jpg/.png/.gif/.webp/.bmp) enviadas como mensajes de imagen, otros archivos como documentos

## Consultar información del grupo

```json
yb_query_group_info({ "group_code": "328306697" })
```

## Miembros de la consulta

|Acción |Descripción |
|--------|-------------|
|`encontrar` |Buscar por nombre (coincidencia parcial, no distingue entre mayúsculas y minúsculas) |
|`lista_bots` |Lista de bots y asistentes de IA de Yuanbao |
|`lista_todo` |Listar todos los miembros |

## Notas

- `group_code` proviene de chat_id: `group:328306697` → `328306697`
- Los grupos se llaman "派 (Pai)" en la aplicación Yuanbao.
- Roles de miembros: `usuario`, `yuanbao_ai`, `bot`