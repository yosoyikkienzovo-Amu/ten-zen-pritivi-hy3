# 🛡️ Amortiguadores Técnicos: Optimización de Carga y Recursos

Para que TEN-ZEN opere con modelos gigantes en hardware de 16GB sin colapsar, implementamos "amortiguadores" (buffers) que suavizan el consumo de RAM y CPU.

## ⚡ 1. Decodificación Especulativa (Speculative Decoding)
Es la técnica de usar una "IA pequeña" para ayudar a una "IA grande".
- **Cómo funciona:** Un modelo muy pequeño (ej. Phi-4 mini 2.5B) genera borradores rápidos de texto. El modelo grande (ej. Llama 3.1 70B) solo verifica y corrige esos borradores.
- **Beneficio:** Aumenta la velocidad de generación hasta en un 2-3x y reduce el tiempo que el modelo grande debe estar activo en RAM.
- **Herramienta:** Soportado nativamente en `llama.cpp` mediante el flag `--speculative`.

## 💾 2. Cuantificación de KV Cache (Memoria de Contexto)
La memoria de la conversación (KV Cache) suele ser el "asesino silencioso" de la RAM.
- **Mejora:** Cuantizar el KV Cache a **4-bit o 8-bit** (en lugar de 16-bit o 32-bit).
- **Impacto:** Reduce a la mitad el consumo de RAM durante conversaciones largas, permitiendo contextos de hasta 32k tokens sin desbordar los 16GB.
- **Herramienta:** Configurable en `Ollama` y `llama.cpp` (`--cache-type-k q4_0`).

## 🗄️ 3. Bases de Datos Vectoriales de Bajo Impacto
Sustituimos bases de datos pesadas por alternativas "in-process" y de ultra-bajo consumo.
- **LanceDB:** Escrita en Rust, es extremadamente rápida y consume una fracción de la RAM que usa ChromaDB o Pinecone. Se integra directamente en el proceso de la IA.
- **DuckDB:** Para la memoria estructurada (tareas, logs), DuckDB es el amortiguador perfecto: rápido, analítico y no requiere un servidor corriendo en segundo plano.

## 🛠️ 4. Orquestación Ligera (Ghost Services)
- **Lazy Loading:** Los servicios (como el servidor MCP o el Bridge) no deben estar "siempre encendidos". Usamos scripts que los levantan solo cuando son llamados y los apagan tras un periodo de inactividad.
- **ZRAM y Swap Dinámico:** Amortiguamos los picos de carga mediante el uso de RAM comprimida en el kernel de Linux (WSL).

---
*Estos amortiguadores permiten que la potencia del gigante no rompa el frágil equilibrio del hardware modesto.*
