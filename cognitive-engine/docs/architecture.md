# Architecture

## Technical Architecture

### System Overview

Cognitive Engine follows a layered architecture optimized for cognitive workflows. Each layer has a single responsibility and communicates through well-defined interfaces.

```
┌─────────────────────────────────────────┐
│           Interface Layer               │
│         (Telegram Bot / API)            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          Application Layer              │
│         (Orchestration / Main)          │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Processing Pipeline             │
│  ┌──────────┬──────────┬─────────────┐  │
│  │ Ingestion│Transcribe│ Reconstruct │  │
│  └──────────┴──────────┴─────────────┘  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Memory Layer                  │
│     (Embeddings / Retrieval / Link)     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Persistence Layer               │
│        (PostgreSQL / PgVector)          │
└─────────────────────────────────────────┘
```

### Component Details

#### 1. Interface Layer

**Purpose:** User interaction and external integrations

**Components:**
- Telegram Bot (`app/bot/`)
- REST API (`app/api/`)

**Responsibilities:**
- Accept voice messages and text input
- Present reconstructed artifacts to users
- Handle authentication and user sessions

#### 2. Application Layer

**Purpose:** Orchestrate the cognitive pipeline

**Components:**
- Main application (`app/main.py`)
- Configuration (`app/config/`)

**Responsibilities:**
- Coordinate data flow between layers
- Manage application lifecycle
- Handle errors and edge cases

#### 3. Processing Pipeline

**Purpose:** Transform raw input into structured knowledge

**Stage 1: Ingestion (`app/ingestion/`)**
- Accept audio files from Telegram
- Download audio from YouTube URLs
- Normalize audio formats
- Store raw data in `data/raw/`

**Stage 2: Transcription (`app/transcription/`)**
- Send audio to Whisper service
- Receive and validate transcripts
- Store in `data/transcripts/`
- Apply initial quality checks

**Stage 3: Reconstruction (`app/reconstruction/`)**
- Clean transcript (remove filler words, false starts)
- Extract key concepts and entities
- Structure into coherent artifacts
- Generate metadata and relationships
- Store in `data/artifacts/`

#### 4. Memory Layer

**Purpose:** Enable semantic retrieval and connection

**Components:**
- Embeddings (`app/memory/embeddings.py`)
- Retrieval (`app/memory/retrieval.py`)
- Linker (`app/memory/linker.py`)

**Responsibilities:**
- Generate vector embeddings for artifacts
- Perform semantic similarity search
- Identify and create connections between artifacts
- Maintain knowledge graph structure

#### 5. Persistence Layer

**Purpose:** Durable storage with semantic capabilities

**Technology Stack:**
- PostgreSQL: Primary database
- PgVector: Vector similarity search
- SQLAlchemy: ORM and query building

**Data Model:**
- Users
- Artifacts
- Concepts
- Relationships
- Embeddings

---

## Data Flow

### Voice-to-Artifact Pipeline

```
1. User sends voice message to Telegram bot
        ↓
2. Bot downloads audio file
        ↓
3. Audio stored in data/raw/
        ↓
4. Whisper transcribes audio → text
        ↓
5. Transcript stored in data/transcripts/
        ↓
6. Cleaner removes noise and filler words
        ↓
7. Extractor identifies concepts and entities
        ↓
8. Structurer organizes into artifact format
        ↓
9. Artifact stored in data/artifacts/ + database
        ↓
10. Embeddings generated and stored in PgVector
        ↓
11. Linker finds related existing artifacts
        ↓
12. Bot responds with structured artifact
```

---

## Design Principles

### 1. Separation of Concerns

Each module has a single responsibility. Changes to transcription logic don't affect reconstruction. Changes to storage don't affect the bot.

### 2. Pipeline Architecture

Data flows through a series of transformations. Each stage is independent and testable. Failures are isolated and recoverable.

### 3. Immutable Artifacts

Once created, artifacts are never modified. Updates create new versions. This enables:
- Audit trails
- Rollback capability
- Temporal queries

### 4. Semantic First

All content is embedded and searchable by meaning, not keywords. This enables:
- Fuzzy matching
- Concept-based retrieval
- Automatic linking

### 5. Minimal Dependencies

Each component depends on abstractions, not implementations. This enables:
- Easy testing with mocks
- Swapping services (e.g., Whisper → alternative)
- Gradual evolution

---

## Technology Choices

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python | Rich AI/ML ecosystem, rapid development |
| Bot Framework | python-telegram-bot | Mature, well-documented, async support |
| Transcription | OpenAI Whisper | Best-in-class accuracy, self-hostable |
| Database | PostgreSQL | Reliability, ACID compliance |
| Vectors | PgVector | Native PostgreSQL extension, no separate service |
| ORM | SQLAlchemy | Type safety, query flexibility |
| Embeddings | Sentence Transformers | Open source, high quality, local execution |

---

## Deployment Architecture

### Development

```
┌─────────────┐
│   Docker    │
│ Compose     │
│             │
│ ┌─────────┐ │
│ │   App   │ │
│ └─────────┘ │
│ ┌─────────┐ │
│ │  Postgres││
│ └─────────┘ │
└─────────────┘
```

### Production (Future)

```
┌─────────────────────────────────┐
│         Load Balancer           │
└───────────────┬─────────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───▼───┐ ┌─────▼─────┐ ┌───▼───┐
│ App 1 │ │   App 2   │ │ App 3 │
└───┬───┘ └─────┬─────┘ └───┬───┘
    │           │           │
    └───────────┼───────────┘
                │
    ┌───────────▼───────────┐
    │    Managed Postgres   │
    │      (with PgVector)  │
    └───────────────────────┘
```

---

## Security Considerations

1. **Data Encryption**
   - All data encrypted at rest
   - TLS for all network communication
   - Environment variables for secrets

2. **Access Control**
   - Telegram user ID as authentication
   - No multi-tenant data access
   - Isolated user namespaces

3. **Privacy**
   - No data shared with third parties (except Whisper if using API)
   - Option for fully local deployment
   - Clear data retention policies

---

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Transcription Latency | < 30s per minute of audio | P95 |
| Reconstruction Time | < 10s per transcript | P95 |
| Search Latency | < 500ms | P99 |
| Availability | 99.9% | Monthly |

---

## Future Considerations

### Scalability
- Horizontal scaling of app instances
- Read replicas for database
- Caching layer for frequent queries

### Extensibility
- Plugin architecture for custom processors
- Webhook support for external integrations
- API for programmatic access

### Observability
- Structured logging
- Metrics collection (Prometheus)
- Distributed tracing