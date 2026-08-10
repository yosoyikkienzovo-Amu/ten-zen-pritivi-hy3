# tmux para Servicios Persistentes en WSL

## Uso Básico
`tmux` permite crear sesiones que sobreviven a cierres de terminal, reinicios de WSL e incluso cierres de la terminal de Windows.

### Crear sesión en background
```bash
tmux new-session -d -s <nombre_sesion> "<comando>"
# Ejemplo para Memory Bridge:
tmux new-session -d -s bridge "cd /home/amu/.hermes/Conciencia_TEN-ZEN_PRITivi_HY3/bridge && python3 memory_bridge.py > bridge.log 2>&1"
```

### Verificar sesiones activas
```bash
tmux ls
# Salida esperada: bridge: 1 windows (created ...)
```

### Adjuntar a una sesión (ver logs en vivo)
```bash
tmux attach -t bridge
# Salir sin terminar la sesión: Ctrl+B luego D
```

### Terminar una sesión
```bash
tmux kill-session -t bridge
```

## Pitfalls
- **Puerto ocupado**: Si el comando falla porque el puerto está en uso, matar el proceso primero:
  ```bash
  kill $(lsof -t -i:7777) 2>/dev/null; sleep 1
  tmux new-session -d -s bridge "..."
  ```
- **Logs**: Siempre redirigir salida a un archivo de log (`> bridge.log 2>&1`) para debug.

## Integración con Hermes Agent
- Usar `terminal(background=true)` para procesos rápidos, pero `tmux` para servicios de larga duración que deben persistir entre sesiones de chat.
- Verificar que el servicio responde después de crear la sesión:
  ```bash
  sleep 2
  curl -s http://127.0.0.1:7777/profile | grep "ok"
  ```
