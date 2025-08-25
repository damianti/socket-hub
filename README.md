# Socket-Hub

Real-time distributed chat application built with microservices architecture.

## Status
🚧 **Work in Progress** - Microservices architecture with Docker Compose implemented

## Overview
Socket-Hub is a real-time chat system designed to handle concurrent connections and distribute load across scalable infrastructure. Similar to WhatsApp/Telegram/Teams.

## Architecture

### Current Implementation
```
┌─────────────────┐
│   React Frontend│ (Port 3000)
└─────────────────┘
        │
┌─────────────────────────┐
│     API Gateway         │ (Port 8000 - External)
│  (WebSocket Manager)    │
└─────────────────────────┘
        │
┌─────────────────────────┐
│    Auth Service         │ (Port 8001 - Internal)
│  (User Authentication)  │
└─────────────────────────┘
        │
┌─────────────────────────┐
│      PostgreSQL         │ (Port 5432 - Internal)
└─────────────────────────┘
```

### Planned Architecture
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
2. **Phase 2**: Authentication & chat rooms ✅
3. **Phase 3**: Microservices & Docker Compose ✅
4. **Phase 4**: Kubernetes deployment 📋

## Local Development

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)

### Quick Start with Docker Compose
```bash
# Clone the repository
git clone <repository-url>
cd socket-hub

# Copy environment files
cp .env.example .env
cp services/auth-service/.env.example services/auth-service/.env

# Update .env files with your configuration
# Edit .env and services/auth-service/.env

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# API Gateway: http://localhost:8000
```

### Manual Development Setup
```bash
# Backend
cd services/api-gateway
uvicorn main:app --reload

# Auth Service
cd services/auth-service
uvicorn main:app --reload --port 8001

# Frontend
cd frontend/web-app
npm start
```

## Contributing
This project is in active development. Check the docs folder for detailed architecture and API documentation.