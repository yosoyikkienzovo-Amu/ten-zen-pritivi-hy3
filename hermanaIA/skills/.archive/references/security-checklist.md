# Lista de verificación de seguridad

Referencia rápida para la seguridad de aplicaciones web.Úselo junto con la habilidad "seguridad y refuerzo".

## Tabla de contenidos

- [Comprobaciones previas al compromiso](#comprobaciones previas al compromiso)
- [Autenticación](#autenticación)
- [Autorización](#autorización)
- [Validación de entrada](#validación de entrada)
- [Encabezados de seguridad](#security-headers)
- [Configuración CORS](#cors-configuration)
- [Protección de datos](#protección-datos)
- [Seguridad de dependencia](#dependencia-seguridad)
- [Manejo de errores] (#control-error)
- [Referencia rápida de los 10 mejores de OWASP] (#owasp-top-10-referencia-rápida)

## Comprobaciones previas al compromiso

- [] No hay secretos en el código (`git diff --cached | grep -i "contraseña\|secret\|api_key\|token"`)
- [ ] `.gitignore` cubre: `.env`, `.env.local`, `*.pem`, `*.key`
- [ ] `.env.example` usa valores de marcador de posición (no secretos reales)

## Autenticación

- [] Contraseñas codificadas con bcrypt (≥12 rondas), scrypt o argon2
- [ ] Cookies de sesión: `httpOnly`, `secure`, `sameSite: 'lax'`
- [] Caducidad de la sesión configurada (edad máxima razonable)
- [] Limitación de velocidad en el punto final de inicio de sesión (≤10 intentos cada 15 minutos)
- [] Tokens de restablecimiento de contraseña: por tiempo limitado (≤1 hora), de un solo uso
- [ ] Bloqueo de cuenta después de repetidos fallos (opcional, con notificación)
- [] MFA compatible con operaciones sensibles (opcional pero recomendado)

## Autorización

- [] Cada punto final protegido verifica la autenticación
- [] Cada acceso a recursos verifica la propiedad/rol (evita IDOR)
- [] Los puntos finales de administración requieren verificación de la función de administrador
- [] Claves API con alcance de permisos mínimos necesarios
- [] Tokens JWT validados (firma, vencimiento, emisor)

## Validación de entrada

- [] Todas las entradas del usuario validadas en los límites del sistema (rutas API, controladores de formularios)
- [] La validación utiliza listas permitidas (no listas prohibidas)
- [] Longitudes de cadena restringidas (mín./máx.)
- [ ] Rangos numéricos validados
- [] Formatos de correo electrónico, URL y fecha validados con bibliotecas adecuadas
- [] Carga de archivos: tipo restringido, tamaño limitado, contenido verificado
- [] Consultas SQL parametrizadas (sin concatenación de cadenas)
- [] Salida HTML codificada (use el marco de escape automático)
- [] URL validadas antes de la redirección (evitar redirección abierta)

## Encabezados de seguridad

```
Política de seguridad de contenido: default-src 'self';script-src 'yo'
Estricta seguridad en el transporte: edad máxima = 31536000;incluirSubDominios
Opciones de tipo de contenido X: nosniff
Opciones de X-Frame: DENEGAR
Protección X-XSS: 0 (deshabilitado, depende de CSP)
Política de referencia: origen-estricto-cuando-origen-cruzado
Política de permisos: cámara=(), micrófono=(), geolocalización=()
```

## Configuración CORS

```mecanografiado
// Restrictivo (recomendado)
cors({
origen: ['https://tudominio.com', 'https://app.tudominio.com'],
credenciales: verdaderas,
métodos: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
Encabezados permitidos: ['Tipo de contenido', 'Autorización'],
})

// NUNCA utilizar en producción:
cors({ origen: '*' }) // Permite cualquier origen
```

## Protección de datos

- [] Campos confidenciales excluidos de las respuestas de API (`passwordHash`, `resetToken`, etc.)
- [] Datos confidenciales no registrados (contraseñas, tokens, números CC completos)
- [] PII cifrada en reposo (si lo exige la normativa)
- [] HTTPS para todas las comunicaciones externas
- [] Copias de seguridad de bases de datos cifradas

## Seguridad de dependencia

```golpecito
# Dependencias de auditoría
auditoría de NPM

# Corregir automáticamente cuando sea posible
corrección de auditoría de npm

# Verificar vulnerabilidades críticas
auditoría npm --nivel de auditoría = crítico

# Mantener las dependencias actualizadas
npx npm-verificar-actualizaciones
```

## Manejo de errores

```mecanografiado
// Producción: error genérico, sin elementos internos
res.status(500).json({
error: {código: 'INTERNAL_ERROR', mensaje: 'Algo salió mal' }
});

// NUNCA en producción:
res.status(500).json({
error: mensaje de error,
pila: err.stack, // Expone las partes internas
consulta: err.sql, // Expone detalles de la base de datos
});
```

## Referencia rápida de los 10 mejores de OWASP

|# |Vulnerabilidad |Prevención |
|---|---|---|
|1 |Control de acceso roto |Verificaciones de autenticación en cada punto final, verificación de propiedad |
|2 |Fallos criptográficos |HTTPS, hash fuerte, sin secretos en el código |
|3 |Inyección |Consultas parametrizadas, validación de entradas |
|4 |Diseño inseguro |Modelado de amenazas, desarrollo basado en especificaciones |
|5 |Configuración incorrecta de seguridad |Encabezados de seguridad, permisos mínimos, departamentos de auditoría |
|6 |Componentes vulnerables |`npm audit`, mantener los departamentos actualizados, departamentos mínimos |
|7 |Fallos de autenticación |Contraseñas seguras, limitación de velocidad, gestión de sesiones |
|8 |Fallos de integridad de datos |Verificar actualizaciones/dependencias, artefactos firmados |
|9 |Fallos de registro |Registre eventos de seguridad, no registre secretos |
|10 |SSRF |Validar/listar direcciones URL permitidas, restringir solicitudes salientes |