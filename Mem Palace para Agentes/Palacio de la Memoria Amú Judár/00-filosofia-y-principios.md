# 00 — Filosofía y Principios No Negociables

Fuente: material técnico provisto directamente por el usuario (contenido tipo CONTRIBUTING.md/README raíz del repo GitHub de MemPalace — no es la página mempalaceofficial.com/concepts/the-palace.html, esa sigue pendiente de lectura).
Registrado: 2026-07-13

## 1. Tesis central
**La memoria es identidad.** Cuando una IA olvida todo entre conversaciones, no puede generar comprensión real — ni del usuario, ni de su trabajo, ni de su gente, ni de su vida. MemPalace existe para resolver eso.

## 2. Qué NO es MemPalace
- No es un motor de búsqueda.
- No es un pipeline de RAG genérico.
- No es un contenedor de base de datos vectorial.

## 3. Qué SÍ es
Un sistema de memoria que trata cada palabra compartida como sagrada: la almacena palabra por palabra y la pone disponible al instante. Los datos nunca salen de la máquina del usuario. Nunca se resume. Nunca se parafrasea. Se devuelven las palabras exactas.

**Recuperación del 100% es el requisito de diseño** — el objetivo contra el que se mide cada ruta de búsqueda. Cualquier cosa por debajo de eso es olvidar, y olvidar es empezar de nuevo.

## 4. Origen del nombre
- **Método de los loci** (miles de años de antigüedad): organizar y recordar grandes volúmenes de información colocándola en habitaciones imaginadas de un edificio imaginado.
- **Zettelkasten** (Niklas Luhmann, sociólogo alemán): fichas pequeñas con referencias cruzadas que se apuntan entre sí.

Aplicación a memoria de IA:
- **Alas (Wings)** → categorías amplias: personas, proyectos, temas.
- **Salas (Rooms)** → agrupaciones por tiempo: días, sesiones.
- **Cajones (Drawers)** → contenido textual completo: las palabras exactas.
- **Compresión AAAK** → capa de índice, formato simbólico compacto (`dialect.py`) que permite a un LLM escanear miles de entradas instantáneamente y saber exactamente qué cajón abrir.

## 5. Los 7 principios de diseño no negociables
Cada PR, cada feature, cada refactor del proyecto debe honrarlos:

1. **Verbatim siempre** — nunca resumir, parafrasear ni comprimir con pérdida los datos del usuario. Se busca en el índice y se devuelven las palabras originales. Promesa fundamental del sistema.
2. **Solo incremental** — ingesta solo de tipo append tras la compilación inicial. Nunca destruir datos existentes para reconstruir. Un accidente a mitad de operación debe dejar intacto el palacio existente.
3. **Entidad primero** — todo codificado por nombres reales, con desambiguación por fecha de nacimiento, ID o contexto. Las personas importan más que los temas.
4. **API externa local-first, cero por defecto** — extracción, fragmentación, embeddings y refinamiento asistido por LLM corren en la máquina del usuario por defecto (Ollama, LM Studio, llama.cpp, vLLM, unsloth studio, etc.). Proveedores externos (Anthropic, OpenAI, Google) soportados vía BYOK, nunca necesarios, nunca habilitados en silencio. El sistema nunca envía contenido del usuario a un servicio que el usuario no haya configurado explícitamente. "LLM local" (Ollama y equivalentes en localhost) NO cuenta como API externa — es parte de la máquina del usuario. BYOK externo siempre es elección deliberada, nunca default, nunca fallback silencioso.
5. **Presupuestos de rendimiento** — hooks por debajo de 500ms. Inyección de arranque por debajo de 100ms. La memoria debe sentirse instantánea.
6. **Privacidad por arquitectura** — el sistema físicamente no puede enviar los datos porque nunca salen de la máquina. Sin telemetría, sin phone-home, sin dependencias de servicios externos para operaciones core.
7. **Todo en segundo plano** — archivado, indexado, timestamps y pipeline corren vía hooks en background. Nada interrumpe la conversación. Cero tokens gastados en "contabilidad" dentro de la ventana de chat.

## 6. Nota para otras instancias de IA
- Estos 7 principios son la constitución técnica del proyecto MemPalace — no son sugerencias.
- El punto 4 (local-first, cero por defecto) es la garantía de que nada de lo que mine el usuario sale de su máquina salvo que él mismo configure explícitamente un backend externo (ver `MEMPALACE_QDRANT_URL` / `MEMPALACE_PGVECTOR_DSN` mencionados en el resumen 01, ambos opt-in explícito).
- El punto 7 (todo en background, cero tokens de contabilidad) es la segunda pieza — junto con `wake-up` y el scoping wing/room (ver resumen 03) — de la estrategia de control de tokens que se venía buscando.
