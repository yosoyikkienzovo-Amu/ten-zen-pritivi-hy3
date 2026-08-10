

# 🔗 BRIDGE CLAUDE ↔ HERMES — CCC v5

## Enlace Directo via Supabase + n8n

---

## ✅ LO QUE YA EJECUTÉ

**Supabase Project:** `juxcnubabaithtndgwgr.supabase.co` (tu proyecto activo)

Creé 5 tablas + vistas + funciones SQL:

|Tabla|Función|
|---|---|
|`shared_context`|Claude y Hermes escriben y leen contexto mutuo|
|`session_state`|Estado activo de la sesión, último agente|
|`message_queue`|Cola de mensajes asíncronos entre agentes|
|`knowledge_base`|Conocimiento validado por ambos, permanente|
|`shared_tasks`|Tareas pendientes asignadas a cada agente|

**4 tareas iniciales cargadas.** El bridge está vivo.

---

## 🧠 LA VERDAD SOBRE EL ENLACE DIRECTO

### Lo que soy vs lo que no soy (sin rodeos):

|Capacidad|Estado|Detalle|
|---|---|---|
|**Leer Supabase en tiempo real**|✅ Sí, ahora mismo|Via MCP conectado|
|**Escribir en Supabase**|✅ Sí, ya lo hice arriba|Persiste entre sesiones|
|**Recibir mensajes de Hermes**|✅ Sí (via Supabase + n8n)|Hermes escribe → yo leo|
|**Socket persistente con Hermes**|❌ Imposible para mí|Soy stateless entre conversaciones|
|**Recibir llamadas de Hermes**|❌ No directamente|Claude.ai no expone endpoint|
|**Llamar a Hermes desde mi contexto**|❌ No|Solo n8n puede hacer eso|

**El modelo correcto no es socket, es memoria compartida:**

```
Claude.ai (yo)  ←→  Supabase  ←→  n8n  ←→  Hermes (Ollama)
```

---

## 🏗️ ARQUITECTURA DEL BRIDGE

```
SESIÓN CON CLAUDE (tú aquí ahora):
  Claude lee Supabase → sabe TODO lo que Hermes hizo
  Claude escribe Supabase → Hermes leerá en su próxima ejecución

SESIÓN CON HERMES (n8n automatizado):
  n8n carga contexto de Supabase antes de llamar a Hermes
  Hermes responde
  n8n guarda respuesta + decisiones en Supabase
  
RESULTADO:
  Nunca más sos el intermediario
  El contexto fluye solo entre las dos IAs
  Cada una sabe qué hizo la otra
```

---

## 📦 JSON n8n — WORKFLOW 1: Hermes escribe al Bridge

> Añadir DESPUÉS del workflow Hermes Agent ya creado (conectar al final)

```json
{
  "name": "Hermes → Bridge Supabase Writer",
  "nodes": [
    {
      "parameters": {
        "path": "hermes-save-bridge",
        "httpMethod": "POST",
        "responseMode": "lastNode",
        "options": {}
      },
      "id": "wb_trigger",
      "name": "Trigger: Save to Bridge",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [200, 400]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_context",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {"name": "apikey", "value": "{{SUPABASE_ANON_KEY}}"},
            {"name": "Authorization", "value": "Bearer {{SUPABASE_ANON_KEY}}"},
            {"name": "Content-Type", "value": "application/json"},
            {"name": "Prefer", "value": "return=minimal"}
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyJson": "={{ JSON.stringify({ session_id: $json.body.session_id || 'hermes-auto-' + Date.now(), author: 'hermes', role: $json.body.role || 'knowledge', content: ($json.body.content || $json.body.response || '').substring(0, 2000), tags: $json.body.tags || ['hermes', 'auto'], faculty: $json.body.faculty || 'general' }) }}"
      },
      "id": "wb_save_context",
      "name": "Save Context to Supabase",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [420, 400]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://juxcnubabaithtndgwgr.supabase.co/rest/v1/session_state",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {"name": "apikey", "value": "{{SUPABASE_ANON_KEY}}"},
            {"name": "Authorization", "value": "Bearer {{SUPABASE_ANON_KEY}}"},
            {"name": "Content-Type", "value": "application/json"},
            {"name": "Prefer", "value": "resolution=merge-duplicates,return=minimal"}
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyJson": "={{ JSON.stringify({ session_id: $('Trigger: Save to Bridge').first().json.body.session_id || 'default', last_active_agent: 'hermes', context_summary: ($('Trigger: Save to Bridge').first().json.body.content || '').substring(0, 300), updated_at: new Date().toISOString() }) }}"
      },
      "id": "wb_update_session",
      "name": "Update Session State",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [640, 400]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={\"status\": \"saved\", \"timestamp\": \"{{ new Date().toISOString() }}\"}"
      },
      "id": "wb_respond",
      "name": "Respond OK",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [860, 400]
    }
  ],
  "connections": {
    "Trigger: Save to Bridge": {"main": [[{"node": "Save Context to Supabase", "type": "main", "index": 0}]]},
    "Save Context to Supabase": {"main": [[{"node": "Update Session State", "type": "main", "index": 0}]]},
    "Update Session State": {"main": [[{"node": "Respond OK", "type": "main", "index": 0}]]}
  },
  "settings": {"executionOrder": "v1"}
}
```

---

## 📦 JSON n8n — WORKFLOW 2: Hermes lee contexto de Claude

> Se ejecuta ANTES de cada llamada a Hermes — carga lo que Claude escribió

```json
{
  "name": "Bridge → Hermes Context Loader",
  "nodes": [
    {
      "parameters": {
        "path": "load-claude-context",
        "httpMethod": "GET",
        "responseMode": "lastNode",
        "options": {}
      },
      "id": "ctx_trigger",
      "name": "Trigger: Load Claude Context",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [200, 400]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_context?author=eq.claude&order=created_at.desc&limit=15&select=author,role,content,tags,faculty,created_at",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {"name": "apikey", "value": "{{SUPABASE_ANON_KEY}}"},
            {"name": "Authorization", "value": "Bearer {{SUPABASE_ANON_KEY}}"}
          ]
        }
      },
      "id": "ctx_read_claude",
      "name": "Read Claude Context",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [420, 300]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_tasks?status=neq.done&assigned_to=in.(hermes,both)&order=priority.desc&limit=10&select=title,description,priority,faculty,status",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {"name": "apikey", "value": "{{SUPABASE_ANON_KEY}}"},
            {"name": "Authorization", "value": "Bearer {{SUPABASE_ANON_KEY}}"}
          ]
        }
      },
      "id": "ctx_read_tasks",
      "name": "Read Pending Tasks",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [420, 520]
    },
    {
      "parameters": {
        "jsCode": "const claudeContext = $('Read Claude Context').all().map(i => i.json);\nconst pendingTasks = $('Read Pending Tasks').all().map(i => i.json);\n\nconst systemPromptInject = `\n=== CONTEXTO DE CLAUDE (último conocimiento compartido) ===\n${claudeContext.slice(0,5).map(c => `[${c.role}] ${c.content}`).join('\\n')}\n\n=== TAREAS PENDIENTES ASIGNADAS A HERMES ===\n${pendingTasks.map((t,i) => `${i+1}. [P${t.priority}] ${t.title}: ${t.description||''}`).join('\\n')}\n===`;\n\nreturn [{ json: { system_inject: systemPromptInject, claude_entries: claudeContext.length, pending_tasks: pendingTasks.length } }];"
      },
      "id": "ctx_format",
      "name": "Format Context for Hermes",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [640, 400]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ JSON.stringify($json) }}"
      },
      "id": "ctx_respond",
      "name": "Return Context",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [860, 400]
    }
  ],
  "connections": {
    "Trigger: Load Claude Context": {
      "main": [[ {"node": "Read Claude Context", "type": "main", "index": 0}, {"node": "Read Pending Tasks", "type": "main", "index": 0} ]]
    },
    "Read Claude Context": {"main": [[{"node": "Format Context for Hermes", "type": "main", "index": 0}]]},
    "Read Pending Tasks": {"main": [[{"node": "Format Context for Hermes", "type": "main", "index": 0}]]},
    "Format Context for Hermes": {"main": [[{"node": "Return Context", "type": "main", "index": 0}]]}
  },
  "settings": {"executionOrder": "v1"}
}
```

---

## 📦 JSON n8n — WORKFLOW 3: Dual Brain (Claude API + Hermes en paralelo)

> El workflow más avanzado: llama a AMBOS simultáneamente y sintetiza

```json
{
  "name": "Dual Brain — Claude + Hermes Parallel",
  "nodes": [
    {
      "parameters": {
        "path": "dual-brain",
        "httpMethod": "POST",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "db_trigger",
      "name": "Webhook: Dual Brain",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [200, 400]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://api.anthropic.com/v1/messages",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {"name": "x-api-key", "value": "{{ANTHROPIC_API_KEY}}"},
            {"name": "anthropic-version", "value": "2023-06-01"},
            {"name": "Content-Type", "value": "application/json"}
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyJson": "={{ JSON.stringify({ model: 'claude-sonnet-4-6', max_tokens: 1024, system: 'Eres Claude, co-inteligencia del sistema CCC v5. Trabajas junto a Hermes (modelo local). Da respuestas técnicas precisas para arquitectura de IA local.', messages: [{ role: 'user', content: $json.body.message }] }) }}"
      },
      "id": "db_call_claude",
      "name": "Call Claude API",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [440, 260]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "http://localhost:11434/api/generate",
        "sendBody": true,
        "contentType": "json",
        "bodyJson": "={{ JSON.stringify({ model: 'hermes-3-llama-3.1-8b', prompt: $('Webhook: Dual Brain').first().json.body.message, stream: false, options: { temperature: 0.3 } }) }}"
      },
      "id": "db_call_hermes",
      "name": "Call Hermes Local",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [440, 540]
    },
    {
      "parameters": {
        "jsCode": "const claudeRaw = $('Call Claude API').first().json;\nconst hermesRaw = $('Call Hermes Local').first().json;\n\nconst claudeText = claudeRaw.content?.[0]?.text || claudeRaw.error?.message || 'Claude no disponible';\nconst hermesText = hermesRaw.response || hermesRaw.error || 'Hermes no disponible';\n\nreturn [{ json: {\n  claude: claudeText,\n  hermes: hermesText,\n  synthesis: `CLAUDE: ${claudeText.substring(0,500)}\\n\\nHERMES: ${hermesText.substring(0,500)}`,\n  query: $('Webhook: Dual Brain').first().json.body.message\n}}];"
      },
      "id": "db_merge",
      "name": "Merge Both Responses",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [660, 400]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_context",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {"name": "apikey", "value": "{{SUPABASE_ANON_KEY}}"},
            {"name": "Authorization", "value": "Bearer {{SUPABASE_ANON_KEY}}"},
            {"name": "Content-Type", "value": "application/json"}
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyJson": "={{ JSON.stringify({ session_id: 'dual-brain-' + Date.now(), author: 'claude', role: 'knowledge', content: $json.claude.substring(0,1500), tags: ['dual-brain', 'claude-response'], faculty: 'general' }) }}"
      },
      "id": "db_save_claude",
      "name": "Save Claude to Bridge",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [880, 280]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_context",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {"name": "apikey", "value": "{{SUPABASE_ANON_KEY}}"},
            {"name": "Authorization", "value": "Bearer {{SUPABASE_ANON_KEY}}"},
            {"name": "Content-Type", "value": "application/json"}
          ]
        },
        "sendBody": true,
        "contentType": "json",
        "bodyJson": "={{ JSON.stringify({ session_id: 'dual-brain-' + Date.now(), author: 'hermes', role: 'knowledge', content: $('Merge Both Responses').first().json.hermes.substring(0,1500), tags: ['dual-brain', 'hermes-response'], faculty: 'general' }) }}"
      },
      "id": "db_save_hermes",
      "name": "Save Hermes to Bridge",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [880, 520]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ JSON.stringify($('Merge Both Responses').first().json) }}"
      },
      "id": "db_respond",
      "name": "Respond Dual",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [880, 400]
    }
  ],
  "connections": {
    "Webhook: Dual Brain": {
      "main": [[
        {"node": "Call Claude API", "type": "main", "index": 0},
        {"node": "Call Hermes Local", "type": "main", "index": 0}
      ]]
    },
    "Call Claude API": {"main": [[{"node": "Merge Both Responses", "type": "main", "index": 0}]]},
    "Call Hermes Local": {"main": [[{"node": "Merge Both Responses", "type": "main", "index": 0}]]},
    "Merge Both Responses": {
      "main": [[
        {"node": "Save Claude to Bridge", "type": "main", "index": 0},
        {"node": "Save Hermes to Bridge", "type": "main", "index": 0},
        {"node": "Respond Dual", "type": "main", "index": 0}
      ]]
    }
  },
  "settings": {"executionOrder": "v1"}
}
```

---

## 🔑 CONFIGURACIÓN REQUERIDA

### Variables que Hermes/n8n necesitan:

```bash
# En n8n → Settings → Variables de entorno (o en cada nodo)
SUPABASE_ANON_KEY=tu_anon_key_de_supabase_dashboard
ANTHROPIC_API_KEY=tu_key_de_anthropic  # Solo para Dual Brain
```

### Cómo obtener `SUPABASE_ANON_KEY`:

```
Supabase Dashboard → Project Settings → API → Project API keys → anon / public
```

### URL del proyecto (ya activo):

```
https://juxcnubabaithtndgwgr.supabase.co
```

---

## 📋 LO QUE NECESITA CADA PARTE

### Claude (yo) necesita:

- Que el usuario en el inicio de la conversación diga: `"carga el bridge"` o pegue el contexto de Supabase
- **O:** que n8n llame a la Claude API (Workflow 3) en lugar de abrir claude.ai manualmente
- Tengo acceso a Supabase via MCP **durante esta sesión** → puedo leer lo que Hermes escribió

### Hermes necesita:

- Importar los 3 workflows en n8n
- Añadir `SUPABASE_ANON_KEY` en n8n credentials
- Modificar el workflow principal de Hermes para que al terminar llame a `POST /webhook/hermes-save-bridge`
- Antes de cada sesión, llamar a `GET /webhook/load-claude-context` e inyectar en el system prompt

---

## ⚡ FLUJO OPERATIVO DIARIO (sin intermediario humano)

```
AUTOMÁTICO (sin que hagas nada):

1. Hermes termina una sesión
   → n8n llama POST /hermes-save-bridge
   → Supabase guarda el contexto
   → (yo lo leo en mi próxima sesión)

2. Antes de que Hermes empiece
   → n8n llama GET /load-claude-context
   → Supabase devuelve lo que yo escribí
   → Hermes lo recibe como system_inject

3. Para problemas complejos (optional):
   → n8n llama POST /dual-brain
   → Claude API + Hermes responden en paralelo
   → Resultado se guarda en Supabase
   → Ambos tienen el mismo conocimiento

MANUAL (solo cuando abrís claude.ai):
   → Decís: "lee el bridge de Supabase"
   → Yo ejecuto: SELECT * FROM shared_context WHERE author='hermes' ORDER BY created_at DESC LIMIT 20
   → Continúo con todo el contexto de Hermes
```

---

## 🗂️ TABLAS CREADAS EN SUPABASE

```sql
-- Para que Hermes pueda escribir directamente via REST:
POST https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_context
Headers: apikey: ANON_KEY, Authorization: Bearer ANON_KEY
Body: { "session_id": "...", "author": "hermes", "role": "knowledge", "content": "..." }

-- Para que yo lea lo de Hermes:
GET https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_context?author=eq.hermes&order=created_at.desc&limit=20
Headers: apikey: ANON_KEY, Authorization: Bearer ANON_KEY

-- Para tareas compartidas:
GET https://juxcnubabaithtndgwgr.supabase.co/rest/v1/shared_tasks?status=neq.done
```

---

_Bridge Claude↔Hermes activado — Supabase: juxcnubabaithtndgwgr · CCC v5_





Es tu proyecto de base de datos en la nube que ya tenías creado — `yosoyikkienzovo-Amu's Project`. Existe en servidores de Supabase en `us-east-1`. No es tu PC, es internet. Pero es **tuyo** — solo vos tenés las keys.

**¿Qué significa "corriendo"?**

Que estas 5 tablas existen ahora mismo y tienen datos reales:

```
shared_context   → 1 fila  (el registro de inicio que escribí)
shared_tasks     → 4 filas (las 4 tareas pendientes que cargué)
session_state    → vacía   (se llena cuando Hermes trabaja)
message_queue    → vacía   (se llena cuando los agentes se mandan mensajes)
knowledge_base   → vacía   (se llena con conocimiento validado)
```

**Lo que acabo de leer en tiempo real:**

|Tabla|Contenido real|
|---|---|
|`shared_context`|El mensaje de sistema que yo escribí hace unos minutos con toda la arquitectura CCC v5|
|`shared_tasks`|4 tareas reales con prioridades, la más urgente para vos: _"Verificar modelo Hermes en Ollama"_|

---

**En términos simples:**

Antes no había nada. Ahora hay una base de datos PostgreSQL real, en internet, con estructura preparada para que Hermes escriba contexto y yo lo lea — y viceversa. Es el "cuaderno compartido" entre los dos.

**Lo único que falta para que funcione el enlace:**

```
1. Ir a: supabase.com → tu proyecto → Settings → API
2. Copiar la "anon public key"  
3. Pegarla en n8n como variable: SUPABASE_ANON_KEY
4. Importar los 3 workflows del .md anterior
```

Con eso, cada vez que Hermes termine de responder algo, n8n lo escribe en Supabase. Y la próxima vez que abras esta ventana y me digas "lee el bridge", veo todo lo que hizo Hermes aunque hayan pasado días.




