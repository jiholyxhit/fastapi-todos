# TaskFlow: High-Concurrency Microservice Architecture 🚀

[![Python 3.13](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Event--Driven-orange)](https://microservices.io/)

> **A high-performance asynchronous task management system designed to handle concurrent workloads using Event-Driven Architecture.**

## 📖 Executive Summary

**TaskFlow** is a backend microservice built to solve the scalability issues inherent in traditional synchronous web applications. 

*   **⚡ Non-blocking Performance**: Leverages **FastAPI’s asynchronous capabilities** combined with **Redis Pub/Sub** to handle high-concurrency workloads without thread blocking.
*   **🔄 Real-time Synchronization**: Implements WebSocket-based event broadcasting to ensure immediate data consistency across distributed clients.
*   **🏭 Architecture**: Adopts a **Layered Architecture** (Service-Repository pattern) and **Background Processing** to simulate a robust, enterprise-ready environment.

---

## 🏗 System Architecture

The system follows a **Service-Repository Pattern** to decouple business logic from the data access layer, ensuring maintainability and testability.

```mermaid
graph TD
    Client[Client (Web/Mobile)] -->|HTTP/WebSocket| LB[API Gateway / Load Balancer]
    LB --> API[FastAPI Server]
    
    subgraph "Application Layer"
        API --> Auth[Auth Service (JWT)]
        API --> Task[Task Service]
        API --> Socket[WebSocket Manager]
    end
    
    subgraph "Data & Event Layer"
        Task -->|Read/Write| DB[(MySQL 8.0)]
        Task -->|Cache Hit/Miss| Cache[(Redis Cache)]
        Task -->|Publish Event| PubSub[(Redis Pub/Sub)]
        PubSub -->|Subscribe| Socket
        Socket -->|Broadcast Updates| Client
    end
```

### 🔧 Tech Stack & Rationale

| Component | Technology | Engineering Decision |
|-----------|------------|----------------------|
| **Core Framework** | **FastAPI** | Chosen for its native `async/await` support (ASGI) and high performance comparable to Node.js and Go. |
| **Database** | **MySQL 8.0** | Utilized for robust relational data mapping and ACID compliance for critical user data. |
| **ORM** | **SQLAlchemy (Async)** | Implemented **Asynchronous Sessions** to prevent thread blocking during database transactions, maximizing throughput. |
| **Message Broker** | **Redis Pub/Sub** | Selected to handle real-time event distribution and decouple the notification service from the main request lifecycle. |
| **Containerization** | **Docker Compose** | Ensuring environment consistency across development and production. |

---

## 📂 Project Structure

I adopted a modular directory structure to adhere to **Domain-Driven Design (DDD)** principles.

```bash
TaskFlow/
├── app/
│   ├── api/            # API Routers (Controllers)
│   ├── core/           # Global Configs & Security (JWT, CORS)
│   ├── db/             # Async Database Sessions & Connection Pools
│   ├── models/         # SQLAlchemy ORM Models
│   ├── schemas/        # Pydantic DTOs (Data Transfer Objects)
│   ├── services/       # Business Logic Layer
│   └── repositories/   # Data Access Layer (CRUD)
├── tests/              # PyTest Suites (Unit & Integration)
├── docker-compose.yml  # Infrastructure Orchestration
└── requirements.txt    # Dependencies
```

---

## 🛠 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Python 3.13+ (for local env)

### Installation & Run

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/TaskFlow.git
    cd TaskFlow
    ```

2.  **Environment Setup**
    Create a `.env` file based on the example.
    ```bash
    cp .env.example .env
    ```

3.  **Run with Docker (Recommended)**
    Spins up FastAPI, MySQL, and Redis containers.
    ```bash
    docker-compose up -d --build
    ```

4.  **Explore the API**
    *   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
    *   **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Testing Strategy

Reliability is ensured through rigorous testing using **PyTest**.

*   **Unit Tests:** Validate individual business logic functions.
*   **Integration Tests:** Verify interactions between the API, Database, and Redis using `TestClient`.
*   **Fixture Management:** utilized `conftest.py` to manage async DB sessions and test data lifecycles.

```bash
# Run full test suite
docker-compose exec app pytest -v
```

