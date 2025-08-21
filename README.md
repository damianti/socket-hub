# Socket-Hub

## 🚀 Chat Distribuido en Tiempo Real

Socket-Hub es una aplicación de chat en tiempo real basada en arquitectura de microservicios. El objetivo es crear un sistema similar a WhatsApp/Telegram/Teams, preparado para manejar conexiones concurrentes y distribuir carga en un entorno escalable.

### 🎯 Objetivos
- Implementar un sistema de chat en tiempo real con WebSockets
- Manejo de conexiones concurrentes con multithreading
- Arquitectura modular de microservicios
- Patrones de diseño: Factory, Observer, Singleton
- Preparado para escalado horizontal con Kubernetes

### 🏗️ Arquitectura
```
┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │  Mobile Client  │
└─────────────────┘    └─────────────────┘
                                │
                    ┌─────────────────────────┐
                    │     API Gateway         │
                    │  (WebSocket Manager)    │
                    └─────────────────────────┘
                                │
    ┌─────────────────────────────────────────────────────────┐
    │                     Redis Pub/Sub                       │
    └─────────────────────────────────────────────────────────┘
                                │
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │ Auth Service│  │Chat Service │  │User Service │
    │             │  │             │  │             │
    └─────────────┘  └─────────────┘  └─────────────┘
                                │
                    ┌─────────────────────────┐
                    │      PostgreSQL         │
                    └─────────────────────────┘
```

### 🛠️ Stack Tecnológico
- **Backend**: FastAPI + WebSockets
- **Base de datos**: PostgreSQL
- **Mensajería**: Redis
- **Contenerización**: Docker + Docker Compose
- **Orquestación**: Kubernetes (futuro)

### 📁 Estructura del Proyecto
```
socket-hub/
├── services/
│   ├── api-gateway/          # API Gateway con WebSockets
│   ├── auth-service/         # Autenticación y autorización
│   ├── chat-service/         # Gestión de salas y mensajes
│   └── user-service/         # Gestión de usuarios
├── shared/
│   ├── models/              # Modelos compartidos
│   ├── utils/               # Utilidades comunes
│   └── config/              # Configuraciones
├── infrastructure/
│   ├── docker/              # Dockerfiles
│   ├── k8s/                 # Kubernetes manifests
│   └── scripts/             # Scripts de deployment
├── docs/                    # Documentación
└── docker-compose.yml       # Orquestación local
```

### 🚀 Desarrollo Incremental
1. **Fase 1**: Estructura base + API Gateway básico
2. **Fase 2**: Auth Service + Chat Service
3. **Fase 3**: Escalabilidad + Kubernetes

### 🏃‍♂️ Ejecutar Localmente
```bash
# Clonar y configurar
git clone <repo>
cd socket-hub

# Ejecutar con Docker Compose
docker-compose up --build
```

### 📚 Documentación
- [Arquitectura](./docs/architecture.md)
- [API Reference](./docs/api.md)
- [Deployment](./docs/deployment.md)