# Recordar Siempre #3: Adaptación de Conocimiento Legado (Windows anterior → Pop!_OS)

Vamos a seguir cruzándonos con archivos del sistema Windows anterior. La regla NO es descartar por ser "de Windows" — es separar patrón transferible de implementación específica de plataforma.

## Flujo obligatorio ante un archivo/protocolo legado:

1. **Separar en dos capas**: (a) el PATRÓN/DISCIPLINA que describe (ej: formato de handoff, taxonomía, checklist) — esto casi siempre es portable; (b) la IMPLEMENTACIÓN técnica específica (rutas Windows, WSL2, PowerShell, IPs de red, netsh) — esto casi nunca lo es.
2. **Clasificar la capa (a)**: ¿el patrón sigue siendo útil en el sistema actual? Si sí, se adapta y se queda. Si no aporta nada nuevo a lo ya existente, se descarta igual que cualquier archivo redundante (Recordar Siempre #2).
3. **Clasificar la capa (b)**: casi siempre se descarta entera si es Windows/WSL2-específica — salvo que el equivalente Linux nativo sea trivial de mapear (ej: mismo comando, distinta ruta).
4. **Nunca archivar credenciales/tokens** encontrados en documentos legado — mismo criterio que Recordar Siempre #2 con Config/auth.json. Reescribir el doc sin el secreto antes de guardarlo.
5. **Nunca asumir que la infraestructura descrita ya existe en el sistema actual** (ej: un plugin, un servicio, un contenedor) — verificar en vivo antes de dar por hecho que algo "ya está instalado" solo porque un doc viejo lo describe.

Ejemplo aplicado (21-jul-2026): protocolo HUELLAS del sistema Windows anterior ("Templo Dell", 7 agentes) → se descarta la mitología de "alma grupal multi-agente" (implementación de un ecosistema que no corre en Pop!_OS), se adapta el formato de footprint de una línea (fecha|agente|misión) como complemento a mempalace_diary_write.
