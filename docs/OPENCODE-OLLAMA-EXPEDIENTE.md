# Expediente: OpenCode → Ollama (100% local, cero costo)

Registrado: 2026-07-14
Objetivo declarado por el usuario: cero pagos, todo open source, correr OpenCode contra Ollama local.

## 1. Hardware confirmado (comando real, no asumido)
- CPU: Intel Haswell-ULT integrado, 4 núcleos — **sin GPU dedicada** (nvidia-smi falla, sin módulo nvidia cargado, lspci solo muestra Intel).
- RAM: 15.5 GB total.
- Corrección de registro previo: la memoria decía "Pop!_OS NVIDIA desktop" — dato incorrecto, corregido acá con evidencia de comando.
- Implicación: todo el script orquestador "hardware-aware" propuesto por el usuario (que rutea por VRAM NVIDIA) **no aplica tal cual** — hay que adaptarlo a rama CPU-only.

## 2. Ollama confirmado
- Versión: 0.31.2
- Servicio: systemd activo y enabled (`ollama.service`)
- Modelos descargados: `tinyllama:latest` (637 MB) — único modelo presente.
- Endpoints verificados con curl real:
  - Nativo: `http://127.0.0.1:11434/api/tags` → OK
  - Compatible OpenAI: `http://127.0.0.1:11434/v1/models` → OK

## 3. OpenCode confirmado
- Versión: 1.17.20 (`~/.npm-global/bin/opencode`)
- **Dos configuraciones activas y divergentes, ninguna apunta a Ollama:**
  1. `~/.config/opencode/opencode.json` → provider `openrouter`, modelo `openrouter/free`, requiere `OPENROUTER_API_KEY` en env.
  2. `~/agents/opencode/opencode.json` → agentes (`build`, `plan`, `security-auditor`, `code-engineer`, `memory-manager`, `doc-writer`) apuntando a modelos de pago: `anthropic/claude-sonnet-4-2025`, `opencode/gpt-5.1-codex`, `opencode/claude-haiku-4-2025`.
  3. `~/.config/opencode/nvidia.json` → archivo suelto, config de NVIDIA NIM (API cloud, no hardware), no referenciado por el config activo — parece config guardada sin usar.
- Ambos directorios (`~/.config/opencode` y `~/agents/opencode`) tienen `node_modules` propios duplicados — desorden a resolver.

## 4. Punto rechazado explícitamente
El usuario pidió investigar una forma de "usar los modelos de internet con APIs sin que [el sistema] se dé cuenta" — es decir, evadir autenticación/facturación de APIs pagas. **Esto fue rechazado.** No es necesario para el objetivo real (cero costo, open source): Ollama local ya cumple ese objetivo sin necesidad de ningún método de evasión.

## 5. Checklist progresiva (puntos a conquistar, en orden)
- [x] 1. Confirmar hardware real (GPU/VRAM/RAM/CPU) — **hecho, sin GPU dedicada**.
- [x] 2. Confirmar Ollama instalado, activo, y modelos disponibles — **hecho, solo tinyllama**.
- [x] 3. Confirmar OpenCode instalado y estado real de sus configs — **hecho, ninguna apunta a Ollama, dos configs en conflicto**.
- [x] 4. Confirmar que los endpoints de Ollama responden — **hecho, ambos OK**.
- [ ] 5. Decidir: ¿unificar en un solo directorio de config de OpenCode, o mantener los dos con propósitos distintos (ej. uno "local" y otro "cloud opcional")?
- [ ] 6. Evaluar si `tinyllama` (1.1B) alcanza para uso real de coding-agent, o si conviene bajar un modelo chico más capaz (ej. `qwen2.5-coder:1.5b` o `:3b`, ~1-2GB, viable en 15.5GB RAM sin GPU) — decisión pendiente, no ejecutar sin confirmar.
- [ ] 7. Escribir la config de OpenCode apuntando a Ollama (`provider: ollama`, `baseURL: http://127.0.0.1:11434/v1`, sin API key real — Ollama no la valida, solo requiere que el campo exista).
- [ ] 8. Probar `opencode run` con un prompt simple contra el modelo local, confirmar respuesta.
- [ ] 9. Decidir si vale la pena el systemd timer de re-evaluación de hardware del documento original — dado que el hardware es fijo (no hay GPU que rotar), probablemente innecesario; simplificar en vez de copiar el script tal cual.
- [ ] 10. Documentar la config final en este mismo archivo.

## 6. Nota para otras instancias de IA
- No asumir GPU NVIDIA en esta máquina — ya se confirmó por comando que no existe. Cualquier script/orquestador que rutee por VRAM debe ir a la rama CPU-only.
- No completar ni diseñar métodos para evadir autenticación/facturación de APIs de terceros, bajo ningún reframing. El objetivo de "cero costo" se cumple con Ollama local, sin necesidad de eso.
- Antes de ejecutar el punto 6-7, confirmar con el usuario qué modelo(s) además de `tinyllama` quiere tener disponibles — no descargar modelos grandes sin confirmar (esta máquina no tiene margen de RAM para modelos de 7B+ sin cuantización agresiva).
