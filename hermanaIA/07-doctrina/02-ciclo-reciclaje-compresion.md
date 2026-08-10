# Recordar Siempre #2: Ciclo de Reciclaje-Compresión de Memoria

Verificado en producción el 21-jul-2026 (purga real de 590/697 drawers + 113 closets huérfanos, integridad ok).

1. **Diagnóstico**: enumerar archivo-fuente único + conteo de drawers (SQL groupby por `source_file`). Nunca juzgar por wing/room agregado — hay que ver el archivo real.
2. **Clasificación explícita por archivo**: ÚTIL / DUDOSO / DESCARTAR. Mostrar la duda, no esconderla ni forzar veredicto sin evidencia.
3. **Confirmación humana explícita antes de borrar.** Una vez dada la orden, ejecutar sin volver a preguntar ítem por ítem.
4. **Backup con checksum SIEMPRE** antes de cualquier borrado masivo (`cp -r` + `md5sum` verificado).
5. **Borrado solo vía API oficial de Chroma** (`collection.get(where=...)` → batches de 500 → `delete`). Nunca tocar `chroma.sqlite3` a mano — rompe la sincronía HNSW/sqlite.
6. **Detectar y limpiar closets huérfanos** en la misma pasada (closet cuyo puntero referencia un drawer_id que ya no existe = residuo, se borra).
7. **Recomprimir automáticamente** el wing afectado al cierre (`mempalace compress --wing X`) para que la capa AAAK quede sincronizada con lo que sobrevivió.
8. **Verificar `sqlite_integrity.ok`** como criterio de éxito real — no "no vi error en pantalla".

Aplica a cualquier decisión de "esto es viejo, esto no sirve, hay que limpiar". No aplica a preguntas sueltas de clasificación de un solo archivo.
