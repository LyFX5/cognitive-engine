# ADR-003: Why PgVector?

**Date:** 2024-01-01  
**Status:** Accepted  
**Authors:** Cognitive Engine Team

## Context

We need to store and query vector embeddings for semantic search. The system must:
- Generate embeddings for all knowledge artifacts
- Perform similarity search efficiently
- Link related concepts across time
- Scale to thousands of vectors per user

## Options Considered

### Option 1: PgVector
PostgreSQL extension for vector similarity search.

**Pros:**
- Native PostgreSQL integration (same database)
- SQL-based queries (no new query language)
- ACID transactions with vector operations
- No additional infrastructure
- Index support (IVFFlat, HNSW)
- Mature and well-maintained
- Open source with no licensing concerns

**Cons:**
- Performance not as optimized as dedicated vector DBs
- Tied to PostgreSQL scaling characteristics
- Newer technology (less battle-tested than core Postgres)

### Option 2: Pinecone
Managed vector database service.

**Pros:**
- Best-in-class performance
- Fully managed (zero ops)
- Built-in scaling
- Excellent documentation

**Cons:**
- Vendor lock-in
- Ongoing cost ($$$ at scale)
- Data leaves our infrastructure
- Another service to manage connections to
- Limited query flexibility compared to SQL

### Option 3: Weaviate
Open-source vector database with hybrid search.

**Pros:**
- Hybrid search (vectors + keywords)
- GraphQL API
- Can self-host or use managed service
- Built-in concept of "classes" (schemas)

**Cons:**
- Separate infrastructure from PostgreSQL
- GraphQL adds complexity
- Need to sync data between Postgres and Weaviate
- Operational overhead of another service

### Option 4: ChromaDB
Lightweight embedding database.

**Pros:**
- Simple API
- Easy to get started
- Good for prototyping
- Can embed in application

**Cons:**
- Less mature than alternatives
- Scaling story unclear
- Not designed for production workloads
- Limited indexing options

### Option 5: Qdrant
Rust-based vector database.

**Pros:**
- High performance
- Rich filtering capabilities
- Self-hostable
- Good API design

**Cons:**
- Separate infrastructure
- Rust ecosystem less familiar to team
- Another service to operate
- Data consistency challenges with separate DB

## Decision

**We chose PgVector.**

## Rationale

### 1. Architectural Simplicity

The most compelling reason: **one database, not two**.

With PgVector:
```sql
-- Find similar artifacts in one query
SELECT a.id, a.content, 
       (e.embedding <=> :query_vector) AS distance
FROM artifacts a
JOIN embeddings e ON a.id = e.artifact_id
WHERE a.user_id = :user_id
ORDER BY distance
LIMIT 10;
```

Without PgVector:
- Query PostgreSQL for metadata
- Query vector DB for similarities
- Join results in application code
- Handle consistency issues

### 2. Transactional Consistency

When we create an artifact:
```python
with session.begin():
    artifact = Artifact(content="...")
    embedding = Embedding(vector=generate_embedding("..."))
    session.add(artifact)
    session.add(embedding)
```

Both succeed or both fail. No orphaned records. No eventual consistency.

With separate databases:
- Distributed transactions are complex
- Rollback across services is error-prone
- Need retry logic and idempotency

### 3. Cost Efficiency

PgVector costs:
- $0 additional (it's free software)
- No extra infrastructure
- No per-vector pricing

Pinecone costs at scale:
- ~$0.06 per 10K vectors/month
- 100K vectors = ~$720/month
- 1M vectors = ~$7,200/month

For a bootstrapped project, this matters.

### 4. Query Flexibility

SQL is powerful. Examples:

**Find recent similar artifacts:**
```sql
SELECT * FROM artifacts a
JOIN embeddings e ON a.id = e.artifact_id
WHERE a.user_id = :user_id
  AND a.created_at > NOW() - INTERVAL '30 days'
ORDER BY e.embedding <=> :query_vector
LIMIT 10;
```

**Find similar artifacts with specific concepts:**
```sql
SELECT a.* FROM artifacts a
JOIN embeddings e ON a.id = e.artifact_id
JOIN artifact_concepts ac ON a.id = ac.artifact_id
JOIN concepts c ON ac.concept_id = c.id
WHERE e.embedding <=> :query_vector < 0.3
  AND c.name IN ('machine learning', 'AI')
ORDER BY e.embedding <=> :query_vector;
```

These queries are harder with separate vector DBs.

### 5. Operational Simplicity

One database means:
- One backup strategy
- One monitoring system
- One connection pool to manage
- One set of credentials
- One disaster recovery plan

For a small team, this is invaluable.

### 6. Performance is "Good Enough"

PgVector performance:
- IVFFlat index: ~10ms for 100K vectors
- HNSW index: ~5ms for 100K vectors
- Our target: < 500ms for search

We're well within requirements. Premature optimization would be wasteful.

## Addressing Concerns

### Performance at Scale

**Concern:** PgVector won't scale like dedicated vector DBs.

**Response:**
- We're not starting at billion-vector scale
- PgVector handles millions of vectors competently
- When we hit limits, we can migrate
- Most applications never outgrow it

### Feature Gap

**Concern:** Dedicated vector DBs have more features.

**Response:**
- We need basic similarity search, not advanced features
- PgVector supports the operations we need
- Can add features later if required
- Simplicity > features for MVP

### Lock-in to PostgreSQL

**Concern:** We're doubling down on PostgreSQL.

**Response:**
- We already chose PostgreSQL (ADR-002)
- This is consistent with that decision
- Vectors are stored as a column type, not proprietary format
- Migration path exists if needed

## Consequences

### Positive
- Simpler architecture
- Lower operational burden
- Better data consistency
- Lower cost
- Unified backup and recovery

### Negative
- Tied to PostgreSQL performance characteristics
- Cannot optimize vector DB independently
- Limited to PgVector's feature set

### Neutral
- Need to learn PgVector-specific indexing strategies
- Must monitor query performance carefully

## Implementation Notes

### Index Strategy

For MVP:
- Use IVFFlat index (faster to build, good enough)
- Revisit HNSW when we have real usage data

### Embedding Dimension

- Using Sentence Transformers: 384 or 768 dimensions
- Store as `vector(768)` in PostgreSQL
- Can adjust if we change embedding models

### Distance Metric

- Cosine similarity (`<=>` operator)
- Most appropriate for text embeddings
- Industry standard for semantic search

## Success Metrics

- Semantic search latency < 100ms (P95)
- Index build time < 1 minute for 10K vectors
- Query accuracy matches dedicated solutions (subjective)
- Zero consistency issues between artifacts and embeddings

## Review Date

This decision will be reviewed when:
- Search latency exceeds 500ms consistently
- We need features PgVector doesn't support
- Vector count exceeds 10 million per user
- Team has capacity to operate separate vector infrastructure

---

*"Simplicity is the ultimate sophistication."* — Leonardo da Vinci