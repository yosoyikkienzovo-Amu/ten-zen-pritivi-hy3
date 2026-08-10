# =======================================================
# CCC v5.2 — IMPORTAR Y ACTIVAR WORKFLOW VIA API LOCAL
# Ejecutar en PowerShell en tu máquina Windows
# =======================================================
# REQUISITO: El archivo JSON debe estar en el mismo directorio
#            O actualiza $jsonPath con la ruta correcta
#
param(
    [string]$jsonPath = ".\CCC_n8n_HermesAgent_v5.2_FIXED.json",
    [string]$n8nUrl  = "http://localhost:5678"
)

$ErrorActionPreference = "Stop"

Write-Host "`n=== CCC v5.2 — Auto Deploy Hermes Agent ===" -ForegroundColor Cyan

# -------------------------------------------------------
# 1. Verificar n8n está vivo
# -------------------------------------------------------
Write-Host "`n[1/5] Verificando n8n..." -ForegroundColor Yellow
try {
    $health = Invoke-WebRequest "$n8nUrl/healthz" -UseBasicParsing -TimeoutSec 5
    Write-Host "  n8n OK ✅ (status $($health.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: n8n no responde en $n8nUrl" -ForegroundColor Red
    Write-Host "  → Ejecutar: docker start n8n" -ForegroundColor Yellow
    exit 1
}

# -------------------------------------------------------
# 2. Leer el JSON del workflow
# -------------------------------------------------------
Write-Host "`n[2/5] Leyendo workflow JSON..." -ForegroundColor Yellow
if (-not (Test-Path $jsonPath)) {
    Write-Host "  ERROR: No encontré $jsonPath" -ForegroundColor Red
    Write-Host "  → Asegúrate de que el JSON esté en la misma carpeta" -ForegroundColor Yellow
    exit 1
}
$workflowJson = Get-Content $jsonPath -Raw -Encoding UTF8
Write-Host "  JSON leído OK ✅ ($([math]::Round(($workflowJson.Length/1KB),1)) KB)" -ForegroundColor Green

# -------------------------------------------------------
# 3. Obtener API key de n8n (buscar en variables de entorno o pedir)
# -------------------------------------------------------
Write-Host "`n[3/5] Configurando autenticación..." -ForegroundColor Yellow

# Intentar obtener la API key guardada
$apiKey = $env:N8N_API_KEY

if (-not $apiKey) {
    Write-Host "  No se encontró N8N_API_KEY en variables de entorno" -ForegroundColor Yellow
    Write-Host "  → Ve a http://localhost:5678 → Settings → API Keys → Create" -ForegroundColor Cyan
    $apiKey = Read-Host "  Pega aquí tu n8n API Key"
}

if (-not $apiKey) {
    Write-Host "  Intentando sin autenticación (n8n sin auth)..." -ForegroundColor Yellow
    $headers = @{ "Content-Type" = "application/json" }
} else {
    Write-Host "  API Key configurada ✅" -ForegroundColor Green
    $headers = @{
        "Content-Type" = "application/json"
        "X-N8N-API-KEY" = $apiKey
    }
}

# -------------------------------------------------------
# 4. Verificar si ya existe el workflow y eliminarlo
# -------------------------------------------------------
Write-Host "`n[4/5] Verificando workflows existentes..." -ForegroundColor Yellow
try {
    $existing = Invoke-RestMethod "$n8nUrl/api/v1/workflows" -Headers $headers -TimeoutSec 10
    $count = if ($existing.data) { $existing.data.Count } else { 0 }
    Write-Host "  Workflows existentes: $count" -ForegroundColor Cyan
    
    # Buscar si ya existe el workflow de Hermes
    if ($existing.data) {
        $hermesWf = $existing.data | Where-Object { $_.name -like "*Hermes*" -or $_.name -like "*CCC*" }
        if ($hermesWf) {
            Write-Host "  Encontrado workflow existente: $($hermesWf.name) (id: $($hermesWf.id))" -ForegroundColor Yellow
            Write-Host "  → Eliminando para reimportar limpio..." -ForegroundColor Yellow
            foreach ($wf in $hermesWf) {
                Invoke-RestMethod "$n8nUrl/api/v1/workflows/$($wf.id)" -Method DELETE -Headers $headers | Out-Null
                Write-Host "    Eliminado: $($wf.name)" -ForegroundColor Gray
            }
        }
    }
} catch {
    Write-Host "  No se pudo listar workflows (posible n8n sin auth configurada)" -ForegroundColor Yellow
}

# -------------------------------------------------------
# 5. Importar workflow
# -------------------------------------------------------
Write-Host "`n[5/5] Importando workflow..." -ForegroundColor Yellow

try {
    $result = Invoke-RestMethod "$n8nUrl/api/v1/workflows" `
        -Method POST `
        -Headers $headers `
        -Body $workflowJson `
        -ContentType "application/json" `
        -TimeoutSec 15
    
    $workflowId = $result.id
    Write-Host "  Workflow importado ✅ (id: $workflowId)" -ForegroundColor Green
    
    # Activar el workflow
    Write-Host "  Activando workflow..." -ForegroundColor Yellow
    $activateBody = '{"active": true}'
    $activated = Invoke-RestMethod "$n8nUrl/api/v1/workflows/$workflowId" `
        -Method PATCH `
        -Headers $headers `
        -Body $activateBody `
        -ContentType "application/json" `
        -TimeoutSec 10
    
    if ($activated.active) {
        Write-Host "  Workflow ACTIVO ✅" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️ Workflow importado pero no se pudo activar automáticamente" -ForegroundColor Yellow
        Write-Host "  → Actívalo manualmente en http://localhost:5678" -ForegroundColor Cyan
    }
    
} catch {
    Write-Host "  ERROR al importar: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Plan B — Importar manualmente:" -ForegroundColor Cyan
    Write-Host "  1. Abre http://localhost:5678"
    Write-Host "  2. Menú (≡) → Import Workflow"
    Write-Host "  3. Seleccionar: CCC_n8n_HermesAgent_v5.2_FIXED.json"
    Write-Host "  4. Activar toggle (esquina superior derecha)"
    exit 1
}

# -------------------------------------------------------
# TEST FINAL
# -------------------------------------------------------
Write-Host "`n=== TEST FINAL ===" -ForegroundColor Cyan
Start-Sleep -Seconds 2

try {
    $testBody = '{"message":"Hermes confirma conexion v5.2 FIXED","faculty":"general","session_id":"auto-deploy-test"}'
    $testResult = Invoke-RestMethod "http://localhost:5678/webhook/hermes" `
        -Method POST `
        -ContentType "application/json" `
        -Body $testBody `
        -TimeoutSec 60
    
    Write-Host "WEBHOOK RESPONDE ✅" -ForegroundColor Green
    Write-Host "  Modelo usado: $($testResult.model_used)" -ForegroundColor Cyan
    Write-Host "  Ollama OK: $($testResult.ollama_ok)" -ForegroundColor Cyan
    Write-Host "  LMStudio OK: $($testResult.lmstudio_ok)" -ForegroundColor Cyan
    Write-Host "  Respuesta: $($testResult.response.Substring(0, [Math]::Min(200, $testResult.response.Length)))..." -ForegroundColor White
} catch {
    Write-Host "Test webhook falló (puede ser que el LLM tarde en responder)" -ForegroundColor Yellow
    Write-Host "→ Probar manualmente en 30s:" -ForegroundColor Cyan
    Write-Host '  Invoke-RestMethod "http://localhost:5678/webhook/hermes" -Method POST -ContentType "application/json" -Body ' -NoNewline
    Write-Host "'"'"'{"message":"test","faculty":"general","session_id":"test-01"}'"'" -ForegroundColor White
}

Write-Host "`n✅ CCC v5.2 Hermes Agent desplegado" -ForegroundColor Green
Write-Host "   Webhook: http://localhost:5678/webhook/hermes" -ForegroundColor Cyan
Write-Host "   Túnel:   https://battle-them-suzuki-representations.trycloudflare.com/webhook/hermes" -ForegroundColor Cyan
