# ResolveAI — AI-Powered Incident Management System

ResolveAI is an AI-assisted incident management platform that transforms unstructured incident reports into structured, prioritized and actionable incidents.

It uses **Google Gemini** to understand natural-language incident reports and extract relevant information. The backend then applies deterministic business rules to calculate incident priority, assign the appropriate support team and maintain an auditable record of incident activities.

The goal is to combine LLM capabilities with reliable backend engineering rather than allowing an AI model to independently control critical business operations.

---

## Key Features

### 1. AI-Powered Incident Assessment

- Accepts incident reports in natural language.
- Uses Google Gemini to extract structured incident information.
- Identifies incident category, location, impact, urgency and deadline.
- Uses structured output and Pydantic validation to validate AI-generated assessments.

### 2. Deterministic Priority Engine

- Calculates incident priority using predefined business rules.
- Uses impact and urgency to determine priority.
- Supports four priority levels:
  - LOW
  - MEDIUM
  - HIGH
  - CRITICAL
- Generates a human-readable explanation for priority decisions.

**Why deterministic logic?**

LLMs are useful for understanding unstructured information, but critical business decisions should be predictable and consistent. ResolveAI therefore separates AI-based assessment from backend-controlled priority calculation.

### 3. Automatic Team Assignment

- Assigns incidents based on predefined category-to-team mappings.
- Uses PostgreSQL to retrieve available support teams.
- Supports categories such as Network, Hardware, Software, Security, Access and Infrastructure.
- Falls back to General Support for other incident categories.

### 4. Incident Management

- Create and retrieve incidents.
- Retrieve individual incident details.
- Update incident information.
- Filter incidents using status and priority.
- Maintain incident ownership through team assignments.

### 5. Idempotent Incident Creation — In Progress

Designed to prevent duplicate incident creation when clients retry requests.

The implementation uses:

- Client-provided idempotency keys.
- SHA-256 request hashing.
- Database uniqueness constraints.
- Duplicate request detection.
- Conflict handling when the same key is reused with different request content.

The end-to-end retry and concurrency scenarios are still being verified.

### 6. Action Logging and Audit Trail

- Maintains an ActionLog associated with incidents.
- Records the initial incident creation event.
- Stores action details and timestamps.
- Designed to support chronological incident activity tracking and resolution verification.

### 7. Incident Lifecycle and Resolution Verification — Planned

The next workflow improvements include:

- Defined incident status transitions.
- Status-change audit events.
- Authorized resolution confirmation.
- Separation of incident resolution from final closure.
- Prevention of invalid status transitions.

---

## System Architecture

ResolveAI follows a modular backend architecture built with FastAPI.

```text
                 Reporter
                    |
                    v
             FastAPI Application
                    |
                    v
             AI Assessment Router
                    |
                    v
              Gemini Service
                    |
                    v
          Structured AI Assessment
                    |
                    v
           Pydantic Validation
                    |
                    v
           Priority Engine
                    |
                    v
         Team Assignment Engine
                    |
                    v
           Incident Service
                    |
                    v
              PostgreSQL
               /       \
              v         v
          Incidents   ActionLog
              |
              v
          Assigned Team
```

### Processing Workflow

1. A reporter submits an incident description.
2. The backend validates the incoming request.
3. The Gemini service analyses the report.
4. Structured output is validated using Pydantic.
5. The Priority Engine calculates the incident priority.
6. The Team Assignment Engine selects an appropriate support team.
7. The Incident Service persists the incident.
8. An initial ActionLog entry is created.
9. The API returns the processed incident information.

**Important design principle:** Gemini performs information extraction and assessment. Priority calculation, team assignment, database persistence and workflow control remain under backend logic.

---

## Technology Stack

| Layer               | Technologies         |
| ------------------- | -------------------- |
| Backend             | Python, FastAPI      |
| AI Integration      | Google Gemini API    |
| Validation          | Pydantic             |
| Database            | PostgreSQL           |
| ORM                 | SQLAlchemy           |
| Database Migrations | Alembic              |
| HTTP Client         | HTTPX                |
| Testing             | Pytest               |
| API Documentation   | Swagger UI / OpenAPI |
| Package Management  | uv                   |

---

## Database Design

ResolveAI currently uses three primary database entities.

### Incident

Stores the main incident information.

Important fields:

- id
- title
- description
- category
- location
- impact
- urgency
- deadline
- priority
- status
- team_id
- idempotency_key
- request_hash
- created_at

### Team

Stores support team information.

Important fields:

- id
- name
- description

### ActionLog

Maintains incident-related activity records.

Important fields:

- id
- incident_id
- action
- details
- timestamp

### Relationships

- One Team can be assigned multiple Incidents.
- One Incident can have multiple ActionLog entries.
- Each ActionLog belongs to one Incident.

---

## Project Structure

```text
Backend/
│
├── migration/
│   ├── versions/
│   └── env.py
│
├── src/
│   └── backend/
│       │
│       ├── core/
│       │   ├── priority_engine.py
│       │   └── team_assignment.py
│       │
│       ├── DB/
│       │   └── database.py
│       │
│       ├── models/
│       │   └── incident.py
│       │
│       ├── routers/
│       │   ├── incident.py
│       │   ├── team.py
│       │   ├── actionLog.py
│       │   └── ai.py
│       │
│       ├── schemas/
│       │   └── ai_assessment.py
│       │
│       ├── services/
│       │   ├── gemini_service.py
│       │   └── incident_service.py
│       │
│       └── main.py
│
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── .env
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.11+
- PostgreSQL
- uv package manager
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/NK1234524/ResolveAI.git
cd ResolveAI/Backend
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the Backend directory.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/resolveai_db
GEMINI_API_KEY=your_gemini_api_key
```

Never commit API keys, database passwords or other secrets to GitHub.

### 4. Configure the Database

Create your PostgreSQL database and apply the migrations:

```bash
uv run alembic upgrade head
```

Make sure the database URL matches your local PostgreSQL configuration.

### 5. Start the Backend Server

From the Backend directory:

```bash
uv run fastapi dev src/backend/main.py
```

### 6. Access API Documentation

Once the server starts, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides interactive documentation for exploring and testing the API endpoints.

---

## API Endpoints

The following are the main API operations currently implemented.

| Method | Endpoint          | Purpose                                            |
| ------ | ----------------- | -------------------------------------------------- |
| POST   | `/ai/assess`      | Analyse a natural-language incident and process it |
| POST   | `/incidents/`     | Create an incident manually                        |
| GET    | `/incidents/`     | Retrieve incidents                                 |
| GET    | `/incidents/{id}` | Retrieve an individual incident                    |
| PATCH  | `/incidents/{id}` | Update incident information                        |
| GET    | `/teams/`         | Retrieve support teams                             |
| GET    | `/action-logs/`   | Retrieve action logs                               |

Refer to Swagger UI for the exact request schemas and available query parameters.

### AI Assessment Example

**Request**

```json
{
  "report": "The Wi-Fi network is not working in classroom 204. Students cannot access online learning resources."
}
```

The `/ai/assess` endpoint also requires an `Idempotency-Key` HTTP header.

The response contains structured incident information, calculated priority, assigned team and incident status.

---

## Engineering Decisions

### AI + Deterministic Backend Logic

The system separates probabilistic AI assessment from deterministic business rules.

Gemini extracts incident information, while the backend independently determines priority and team assignment.

### Database Transactions

Incident creation and its initial ActionLog entry are persisted within the same database transaction to maintain consistency.

### Idempotency

Idempotency keys and request hashes are being implemented to make incident creation safer when clients retry requests.

### Modular Architecture

Responsibilities are separated into routers, schemas, services, models and core business logic to improve maintainability and testability.

---

## Current Development Status

| Component                           | Status                                  |
| ----------------------------------- | --------------------------------------- |
| FastAPI application setup           | Complete                                |
| PostgreSQL integration              | Complete                                |
| SQLAlchemy models                   | Complete                                |
| Alembic migrations                  | Complete                                |
| Incident CRUD APIs                  | Complete                                |
| Gemini integration                  | Implemented                             |
| Structured AI assessment            | Implemented                             |
| Priority Engine                     | Implemented and unit-tested             |
| Automatic team assignment           | Implemented                             |
| Initial ActionLog creation          | Implemented                             |
| Idempotency                         | Implemented, end-to-end testing pending |
| Authentication and RBAC             | Planned                                 |
| Complete audit workflow             | In progress                             |
| Resolution verification             | Planned                                 |
| Deployment and production hardening | Planned                                 |

---

## Future Improvements

- Authentication and role-based access control.
- Complete incident lifecycle management.
- Resolution verification and authorization.
- Comprehensive integration and concurrency testing.
- Gemini timeout handling, retries and fallback strategy.
- Improved audit logging with actor and action-result information.
- Frontend dashboard for reporters, responders and administrators.
- Deployment and monitoring.

---

## Project Objective

ResolveAI explores how Large Language Models can be integrated into practical enterprise workflows while maintaining predictable business logic, data consistency and operational control.

The project focuses on building an AI-assisted backend system that does more than generate text: it converts unstructured information into validated, actionable and traceable operations.

---

**Developed as an independent software engineering project.**


