# Socket-Hub

Real-time distributed chat application built with microservices architecture.

## Status
🚧 **Work in Progress** - Currently implementing core WebSocket functionality

## Overview
Socket-Hub is a real-time chat system designed to handle concurrent connections and distribute load across scalable infrastructure. Similar to WhatsApp/Telegram/Teams.

## Architecture
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
    └─────────────┘  └─────────────┘  └─────────────┘
                                │
                    ┌─────────────────────────┐
                    │      PostgreSQL         │
                    └─────────────────────────┘
```

## Tech Stack
- **Backend**: FastAPI + WebSockets
- **Database**: PostgreSQL
- **Messaging**: Redis
- **Frontend**: React + TypeScript
- **Containerization**: Docker
- **Orchestration**: Kubernetes (planned)

## Project Structure
```
socket-hub/
├── services/
│   ├── api-gateway/          # WebSocket API Gateway
│   ├── auth-service/         # Authentication
│   ├── chat-service/         # Chat management
│   └── user-service/         # User management
├── frontend/
│   └── web-app/             # React frontend
├── shared/
│   ├── models/              # Shared models
│   ├── utils/               # Utilities
│   └── config/              # Configuration
├── infrastructure/
│   ├── docker/              # Dockerfiles
│   ├── k8s/                 # Kubernetes manifests
│   └── scripts/             # Deployment scripts
└── docs/                    # Documentation
```

## Development Phases
1. **Phase 1**: Basic WebSocket functionality ✅
2. **Phase 2**: Authentication & chat rooms 🚧
3. **Phase 3**: Microservices & scaling 📋

## Local Development
```bash
# Backend
cd services/api-gateway
uvicorn main:app --reload

# Frontend
cd frontend/web-app
npm start
```

## Contributing
This project is in active development. Check the docs folder for detailed architecture and API documentation.