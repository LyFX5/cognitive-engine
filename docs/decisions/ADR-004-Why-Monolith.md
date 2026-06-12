# ADR-004: Why Monolith?

**Date:** 2024-01-01  
**Status:** Accepted  
**Authors:** Cognitive Engine Team

## Context

We need to decide on the architectural style for Cognitive Engine. The system will:
- Process voice messages asynchronously
- Run multiple pipeline stages (ingestion, transcription, reconstruction, embedding)
- Serve a Telegram bot interface
- Provide API endpoints for future integrations

The team is small (1-3 developers initially), and we need to move fast.

## Options Considered

### Option 1: Monolithic Architecture
Single codebase, single deployment unit.

**Pros:**
- Simple development workflow
- Easy to debug (no distributed tracing needed)
- Atomic deployments
- No network overhead between components
- Single database connection pool
- Easier testing (no mocking external services)
- Lower operational complexity
- Faster iteration speed

**Cons:**
- Can become unwieldy as it grows
- Scaling requires replicating entire application
- Technology stack must be uniform
- Risk of tight coupling between modules

### Option 2: Microservices Architecture
Separate services for each major function.

**Example breakdown:**
- Bot Service (Telegram handling)
- Transcription Service (Whisper integration)
- Reconstruction Service (LLM processing)
- Memory Service (embeddings and search)
- API Service (REST endpoints)

**Pros:**
- Independent scaling per service
- Technology flexibility per service
- Fault isolation
- Team autonomy at scale

**Cons:**
- High operational complexity
- Distributed system challenges (network failures, retries, idempotency)
- Complex deployments (orchestration needed)
- Inter-service communication overhead
- Data consistency challenges
- Requires DevOps expertise
- Slower iteration speed

### Option 3: Modular Monolith
Single deployment with clear module boundaries.

**Pros:**
- All benefits of monolith (simplicity, speed)
- Clear separation of concerns
- Easier to extract services later if needed
- Enforced architectural boundaries

**Cons:**
- Still has monolith scaling limitations
- Requires discipline to maintain boundaries
- Slightly more upfront design needed

### Option 4: Serverless/Event-Driven
Functions-as-a-Service for pipeline stages.

**Pros:**
- Pay-per-execution pricing
- Automatic scaling
- No server management

**Cons:**
- Cold start latency issues
- Vendor lock-in (AWS Lambda, etc.)
- Complex state management
- Debugging difficulties
- Cost unpredictable at scale

## Decision

**We chose Modular Monolith.**

## Rationale

### 1. Team Size and Velocity

We are a small team building an MVP. Our priority is:
- Fast iteration
- Quick feedback loops
- Minimal operational overhead

A monolith enables this. Microservices would slow us down with:
- Service coordination
- Integration testing complexity
- Deployment orchestration

As Jeff Bezos noted, microservices are about team scaling, not technical necessity. We don't have 100+ engineers.

### 2. Premature Optimization

Common argument for microservices: "We need to scale."

Reality check:
- We don't have scale problems yet
- Most applications never need microservices
- Monoliths can handle significant load (properly designed)
- When we hit limits, we'll have real data to guide decisions

Scaling a monolith:
- Vertical: Add more CPU/RAM
- Horizontal: Run multiple instances behind load balancer
- Database: Read replicas, connection pooling

This gets us far. Very far.

### 3. Complexity Budget

Every project has a complexity budget. You can spend it on:
- Business logic (understanding user needs, building features)
- Infrastructure (distributed systems, orchestration, networking)

We choose to spend our budget on:
- Cognitive reconstruction algorithms
- Semantic understanding
- User experience

Not on:
- Service mesh configuration
- Distributed tracing setup
- Cross-service transaction management

### 4. Testing Simplicity

Monolith testing:
```python
def test_voice_to_artifact():
    result = process_voice("test_audio.mp3")
    assert result.artifact_type == "insight"
```

Microservices testing:
```python
def test_voice_to_artifact():
    # Mock transcription service
    # Mock reconstruction service
    # Mock embedding service
    # Handle network timeouts
    # Handle partial failures
    # Test retry logic
    # ...
```

The difference is stark.

### 5. Deployment Simplicity

Monolith deployment:
```bash
docker-compose up
```

Microservices deployment:
- Kubernetes cluster
- Service definitions
- Ingress configuration
- Health checks per service
- Rolling update strategies
- Monitoring per service

For MVP, the choice is obvious.

### 6. Extracting Services Later

A well-designed monolith can evolve:
1. Identify natural boundaries (we already have them)
2. Measure actual load patterns
3. Extract hot spots when needed
4. Migrate incrementally

This is easier than:
- Starting with microservices
- Dealing with premature abstraction
- Re-integrating poorly bounded services

## Addressing Concerns

### "Monoliths Don't Scale"

**Response:** This is a myth. Examples:
- GitHub ran as Ruby monolith for years at massive scale
- Shopify still largely monolithic
- Stack Overflow handles billions of requests as .NET monolith

The bottleneck is usually the database, not application architecture.

### "We Need Fault Isolation"

**Response:** 
- Proper error handling within monolith provides isolation
- Circuit breakers can be implemented internally
- Process boundaries (separate workers) can isolate failures
- For MVP, uptime requirements don't justify microservices complexity

### "Different Components Have Different Needs"

**Response:**
- True, but this doesn't require separate services
- Use async workers for heavy tasks (Celery, RQ)
- Use different process types in Docker
- Internal queues for load leveling

### "Microservices Enable Team Autonomy"

**Response:**
- Conway's Law works both ways
- Small teams benefit from shared codebase
- Communication overhead is low with 1-3 people
- Can reorganize when team grows

## Consequences

### Positive
- Faster development velocity
- Simpler testing strategy
- Easier debugging
- Lower operational burden
- Reduced infrastructure cost
- Clearer code ownership

### Negative
- Single point of failure (mitigated by proper deployment)
- Scaling less granular (but adequate for foreseeable future)
- Must resist temptation to over-engineer

### Neutral
- Need discipline to maintain module boundaries
- Must monitor for natural extraction points
- Should document module interfaces clearly

## Module Boundaries

Our monolith has clear internal boundaries:

```
app/
├── bot/           # Telegram interface
├── ingestion/     # Audio capture
├── transcription/ # Speech-to-text
├── reconstruction/# Semantic processing
├── memory/        # Embeddings and retrieval
├── database/      # Data persistence
├── api/           # REST endpoints
└── shared/        # Common utilities
```

Each module:
- Has a single responsibility
- Communicates through defined interfaces
- Can be tested in isolation
- Could become a service later if needed

## When to Reconsider

This decision should be reviewed when:
- Team grows beyond 8-10 developers
- Specific component becomes a clear bottleneck
- Different components need vastly different tech stacks
- Regulatory requirements demand isolation
- We have dedicated DevOps team

Even then, extraction should be:
- Data-driven (based on actual metrics)
- Incremental (one service at a time)
- Justified (clear ROI)

## Success Metrics

- Development velocity: Feature completion < 1 week
- Deployment frequency: Multiple times per day
- Mean time to recovery: < 1 hour
- Codebase comprehension: New developer productive in < 1 week

---

*"Monoliths are not evil. Poorly designed systems are."* — Martin Fowler