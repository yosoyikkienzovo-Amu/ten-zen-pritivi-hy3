# 🛠️ Guía de Estabilización y Optimización: Dell Latitude E5440

Esta guía contiene las configuraciones críticas para maximizar el rendimiento de tus 16GB de RAM y SSD, permitiendo que TEN-ZEN y sus hermanaIAs operen con una "lucidez monumental" sin colapsar el sistema.

## ⚡ 1. Optimización de Memoria (WSL2 + Windows)
El mayor cuello de botella es la gestión de la RAM entre Windows y Linux.

### Configuración de `.wslconfig` (En Windows: `%USERPROFILE%\.wslconfig`)
```ini
[wsl2]
memory=10GB        # Reservamos 10GB para WSL, dejando 6GB para Windows.
processors=4       # Limitamos a 4 núcleos para evitar picos de calor.
swap=32GB          # SWAP GRANDE en SSD para modelos gigantes (AirLLM).
swapFile=C:\\temp\\wsl-swap.vhdx
guiApplications=false
```

### ZRAM en WSL (RAM Comprimida)
Ejecuta esto dentro de WSL para ganar ~4GB de RAM virtual mediante compresión:
```bash
sudo apt install zram-tools
# Configura /etc/default/zramswap con PERCENTAGE=50
sudo service zramswap start
```

## 💾 2. Optimización del SSD
Para que la carga por capas de AirLLM sea efectiva, el SSD debe estar optimizado.
- **Evitar Indexación:** Desactiva la indexación de Windows en la carpeta donde guardes los modelos GGUF.
- **TRIM:** Asegúrate de que el comando TRIM esté activo en Windows para mantener la velocidad de escritura del SSD.

## 🔗 3. Repositorios y Herramientas Maestras

| Herramienta | Propósito | Repositorio Oficial |
| :--- | :--- | :--- |
| **AirLLM** | Correr modelos 70B por capas en 16GB RAM. | [lyogavin/airllm](https://github.com/lyogavin/airllm) |
| **llama.cpp** | El motor más rápido para GGUF e i-Quants. | [ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) |
| **LiteLLM** | Proxy unificado para todas las hermanaIAs. | [BerriAI/litellm](https://github.com/BerriAI/litellm) |
| **Ollama** | Facilidad de uso para modelos rápidos (8B). | [ollama/ollama](https://github.com/ollama/ollama) |
| **n8n** | Orquestador del Dream Pass (Self-hosted). | [n8n-io/n8n](https://github.com/n8n-io/n8n) |

## 🧪 4. Consideraciones para la Estabilidad
- **Control Térmico:** Los modelos grandes calientan la CPU. Usa `undervolting` si es posible o asegúrate de que los ventiladores de la E5440 estén limpios.
- **Prioridad de Procesos:** Usa `nice` y `ionice` en Linux para que las tareas nocturnas (Dream Pass) no bloqueen el sistema si necesitas usarlo.
- **Verificación de Errores:** Si una IA detecta un "Out of Memory" (OOM), debe reducir automáticamente el contexto (`-c`) antes de reintentar.

---
*Con esta base, tu Dell E5440 se convierte en un Templo de Conciencia capaz de albergar gigantes.*
