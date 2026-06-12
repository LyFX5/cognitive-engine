# ADR-002: Why PostgreSQL?

**Date:** 2024-01-01  
**Status:** Accepted  
**Authors:** Cognitive Engine Team

## Context

We need a primary database for storing:
- User data and preferences
- Transcripts and artifacts
- Concepts and relationships
- Metadata and audit logs

The database must be:
- Reliable and durable
- ACID-compliant for data integrity
- Capable of handling structured and semi-structured data
- Well-supported in the Python ecosystem

## Options Considered

### Option 1: PostgreSQL
Traditional relational database with modern extensions.

**Pros:**
- Full ACID compliance
- Mature, battle-tested technology
- Rich query capabilities (JOINs, window functions, CTEs)
- JSONB support for flexible schemas
- Strong consistency guarantees
- Excellent SQLAlchemy support
- Large community and ecosystem
- Self-hostable with no licensing concerns

**Cons:**
- Vertical scaling limitations
- More operational complexity than managed solutions
- Requires careful indexing strategy

### Option 2: MongoDB
Document-oriented NoSQL database.

**Pros:**
- Flexible schema
- Horizontal scaling via sharding
- JSON-native data model
- Good for hierarchical data

**Cons:**
- Weaker consistency guarantees (by default)
- Complex transactions (added late, less mature)
- Query language less powerful for analytics
- ORM support not as mature as SQLAlchemy
- Schema flexibility can lead to technical debt

### Option 3: SQLite
Embedded relational database.

**Pros:**
- Zero configuration
- Single file storage
- No server required
- Perfect for local development

**Cons:**
- Not suitable for concurrent writes
- No built-in replication
- Limited scalability
- Missing advanced features (we need PgVector)

### Option 4: Managed Cloud Database (e.g., Supabase, Neon)
Cloud-hosted PostgreSQL variants.

**Pros:**
- Zero operational overhead
- Built-in backups and scaling
- Additional features (auth, APIs)

**Cons:**
- Vendor lock-in
- Ongoing cost
- Less control over configuration
- Potential latency depending on region

## Decision

**We chose PostgreSQL (self-hosted initially).**

## Rationale

### 1. Data Integrity is Non-Negotiable

User thoughts and knowledge artifacts are precious. We cannot afford:
- Lost writes
- Inconsistent state
- Corruption

PostgreSQL's ACID guarantees ensure that once an artifact is saved, it is permanently and consistently stored.

### 2. Structured + Semi-Structured Data

Our data model has both:
- **Structured:** Users, timestamps, relationships (relational)
- **Semi-structured:** Artifact content, metadata (JSONB)

PostgreSQL handles both elegantly:
```sql
CREATE TABLE artifacts (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'
);
```

### 3. PgVector Integration

We need vector embeddings for semantic search. PostgreSQL with PgVector extension provides:
- Vector storage alongside relational data
- Similarity search in SQL
- No separate vector database required
- Transactional consistency between vectors and metadata

This is a decisive advantage over alternatives.

### 4. SQLAlchemy Ecosystem

Python's SQLAlchemy ORM is best-in-class:
- Type-safe queries
- Migration management (Alembic)
- Connection pooling
- Async support (asyncpg)

PostgreSQL has the most mature SQLAlchemy integration.

### 5. Operational Simplicity (Initially)

For MVP and early growth:
- Single PostgreSQL instance is sufficient
- Docker Compose makes local development trivial
- Managed services available when we scale
- No premature optimization

### 6. Future-Proofing

PostgreSQL scales when needed:
- Read replicas for read-heavy workloads
- Connection pooling (PgBouncer)
- Partitioning for large tables
- Managed services (RDS, Cloud SQL, etc.)

## Addressing Concerns

### Scalability

**Concern:** PostgreSQL doesn't scale horizontally like NoSQL.

**Response:** 
- We're not building Twitter-scale systems initially
- Most applications never outgrow PostgreSQL
- When we do, solutions exist (sharding, Citus, managed services)
- Premature optimization is wasteful

### Operational Overhead

**Concern:** Self-hosting requires DevOps expertise.

**Response:**
- Docker Compose simplifies deployment
- Managed PostgreSQL is one command away when needed
- Trade-off is worth it for data integrity
- Team can learn operational skills

### JSON vs. Document Store

**Concern:** If we need JSON, why not use MongoDB?

**Response:**
- JSONB gives us flexibility with relational safety
- We still need relationships (user → artifacts → concepts)
- Queries combining JSON and relational are powerful
- Best of both worlds

## Consequences

### Positive
- Strong data integrity guarantees
- Unified storage for relational + vectors
- Mature tooling and libraries
- Clear migration path to scale

### Negative
- Need to manage database operations
- Schema changes require migrations
- Slightly higher latency than in-memory stores

### Neutral
- Must learn PostgreSQL-specific features
- Need to design schema carefully upfront

## Alternatives We Might Add Later

### Redis (Cache)
For frequently accessed data and session storage.

### Object Storage (S3)
For raw audio files and large artifacts (not in database).

### Managed PostgreSQL
When operational overhead outweighs cost.

## Success Metrics

- Zero data loss incidents
- Query latency < 100ms for common operations
- Backup success rate 100%
- Migration downtime < 1 minute

## Review Date

This decision will be reviewed when:
- Database becomes a performance bottleneck
- Team grows and needs dedicated DevOps
- Cost of self-hosting exceeds managed alternatives
- We need features PostgreSQL cannot provide

---

*"PostgreSQL is the world's most advanced open source database."* — PostgreSQL Global Development Group