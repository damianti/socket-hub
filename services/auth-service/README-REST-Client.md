# Auth Service - REST Client Testing

Este directorio contiene archivos para probar los endpoints del auth-service usando la extensión REST Client de VS Code.

## Archivos Disponibles

### 1. `auth-service.http`
Archivo básico con URLs hardcodeadas para pruebas rápidas.

### 2. `auth-service-with-env.http`
Archivo avanzado que usa variables de entorno para mayor flexibilidad.

### 3. `.vscode/settings.json`
Configuración de VS Code para mejorar la experiencia de REST Client.

## Instalación

1. **Instalar la extensión REST Client en VS Code:**
   - Buscar "REST Client" en el marketplace
   - Instalar la extensión de Huachao Mao

2. **Configurar el entorno:**
   - Abrir el archivo `.http` en VS Code
   - En la esquina inferior derecha, seleccionar el entorno:
     - `local` para desarrollo local (http://localhost:8001)
     - `docker` para entorno Docker (http://auth-service:8001)

## Cómo Usar

### Método 1: Archivo Básico
1. Abrir `auth-service.http`
2. Hacer clic en "Send Request" sobre cualquier endpoint
3. Ver la respuesta en el panel derecho

### Método 2: Archivo con Variables de Entorno
1. Abrir `auth-service-with-env.http`
2. Seleccionar el entorno (local/docker) en la esquina inferior derecha
3. Hacer clic en "Send Request" sobre cualquier endpoint

## Endpoints Incluidos

### Health Checks
- `GET /` - Health check principal
- `GET /health/` - Health check específico

### Autenticación
- `POST /auth/signup` - Registro de usuarios
- `POST /auth/login` - Inicio de sesión

### Documentación
- `GET /docs` - Documentación Swagger
- `GET /openapi.json` - Esquema OpenAPI

## Casos de Prueba

### Casos Exitosos
1. **Signup básico** - Usuario válido
2. **Login correcto** - Credenciales válidas
3. **Múltiples usuarios** - Varios registros

### Casos de Error
1. **Credenciales incorrectas** - Login fallido
2. **Usuario inexistente** - Login con usuario que no existe
3. **Username duplicado** - Registro con username existente
4. **Email duplicado** - Registro con email existente
5. **Email inválido** - Formato de email incorrecto
6. **Campos vacíos** - Validación de campos requeridos
7. **Contraseña corta** - Validación de longitud mínima

### Casos Edge
1. **Caracteres especiales** - Usernames y emails con caracteres especiales
2. **Campos largos** - Validación de límites de longitud
3. **Caracteres Unicode** - Soporte para caracteres internacionales

## Variables de Entorno Disponibles

### Local Environment
```json
{
    "baseUrl": "http://localhost:8001",
    "authServiceUrl": "http://localhost:8001"
}
```

### Docker Environment
```json
{
    "baseUrl": "http://postgres:5432",
    "authServiceUrl": "http://auth-service:8001"
}
```

## Comandos Útiles

### Ejecutar Todos los Requests
- `Ctrl+Shift+P` → "REST Client: Run All Requests"

### Ejecutar Request Específico
- Hacer clic en "Send Request" sobre el endpoint deseado

### Cambiar Entorno
- Hacer clic en el selector de entorno en la esquina inferior derecha

## Respuestas Esperadas

### Signup Exitoso
```json
{
    "id": "uuid-string",
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2025-08-26T18:29:01.165654+03:00"
}
```

### Login Exitoso
```json
{
    "id": "uuid-string",
    "username": "testuser",
    "email": "test@example.com",
    "created_at": "2025-08-26T18:29:01.165654+03:00"
}
```

### Health Check
```json
{
    "message": "auth is running",
    "status": "healthy"
}
```

## Troubleshooting

### Error de Conexión
- Verificar que el auth-service esté corriendo en el puerto correcto
- Verificar que PostgreSQL esté funcionando
- Revisar la configuración de la base de datos

### Error de Permisos
- Verificar que el usuario `damian` tenga permisos en la base de datos
- Ejecutar los comandos de configuración de permisos si es necesario

### Variables de Entorno No Resueltas
- Verificar que el archivo `.vscode/settings.json` esté configurado correctamente
- Seleccionar el entorno correcto en VS Code
