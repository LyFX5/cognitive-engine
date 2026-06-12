# Cognitive Engine

## What is this?

Cognitive Engine is an AI-native system that transforms spoken thoughts into structured, reusable knowledge. It is designed for founders, researchers, engineers, writers, and systems thinkers who generate ideas faster than they can organize them.

The goal is not note-taking.  
The goal is semantic reconstruction of thought.

---

## Why?

Most ideas disappear.  
Not because they are bad.  
Because they never survive the transition from working memory to durable knowledge.

---

## Product Positioning

**Not:**
- AI chatbot
- Note-taking application
- Meeting transcription tool

**Instead:**
- Cognitive interface
- Thought reconstruction system
- Personal knowledge infrastructure

---

## MVP v0.1 Features

✓ Telegram voice capture  
✓ Speech transcription  
✓ Semantic cleanup  
✓ Structured artifact generation  
✓ Concept extraction  
✓ Semantic search  

---

## Architecture

```
Telegram
   ↓
Ingestion
   ↓
Whisper
   ↓
Reconstruction
   ↓
Knowledge Artifact
   ↓
Embeddings
   ↓
Memory
```

---

## Repository Structure

### `app/` — Core Application Logic

The heart of the Cognitive Engine. Every module serves a specific cognitive function.

#### `app/main.py`
Application entry point. Orchestrates the pipeline from voice input to knowledge artifact.

#### `app/config/` — Configuration & Environment
**Why:** Centralized configuration management ensures consistent behavior across environments and simplifies deployment.
- `settings.py` — Environment variables and application settings
- `logging.py` — Logging configuration for observability

#### `app/bot/` — Telegram Bot Interface
**Why:** Provides the cognitive interface layer where users interact with the system through natural voice and text.
- `handlers/` — Message and command handlers (start, voice, text)
- `keyboards/` — Inline and reply keyboards for user interaction
- `bot.py` — Bot initialization and configuration

#### `app/ingestion/` — Content Ingestion
**Why:** Captures raw cognitive input from multiple sources, preserving the original signal before transformation.
- `audio_loader.py` — Handles audio file uploads
- `youtube_loader.py` — Fetches audio from YouTube URLs

#### `app/transcription/` — Speech-to-Text
**Why:** Converts ephemeral speech into persistent text, the first step in making thoughts durable.
- `whisper_service.py` — Whisper API integration for transcription
- `schemas.py` — Data models for transcription results

#### `app/reconstruction/` — Semantic Reconstruction
**Why:** Transforms raw transcripts into structured knowledge artifacts. This is where thought becomes knowledge.
- `cleaner.py` — Removes filler words, false starts, and noise
- `extractor.py` — Extracts key concepts, entities, and relationships
- `structurer.py` — Organizes content into coherent structures
- `prompts.py` — LLM prompts for reconstruction tasks
- `schemas.py` — Data models for reconstructed artifacts

#### `app/memory/` — Knowledge Memory
**Why:** Enables semantic retrieval and connection of ideas across time. This is what makes knowledge reusable.
- `embeddings.py` — Generates vector embeddings for semantic search
- `retrieval.py` — Retrieves relevant knowledge based on queries
- `linker.py` — Connects related concepts and artifacts

#### `app/database/` — Data Persistence
**Why:** Durable storage for all cognitive artifacts and their relationships.
- `models.py` — SQLAlchemy ORM models
- `session.py` — Database session management
- `repositories/` — Data access layer for business logic

#### `app/api/` — HTTP API
**Why:** Exposes system capabilities to external clients and integrations.
- `health.py` — Health check endpoints

#### `app/shared/` — Shared Utilities
**Why:** Common types, exceptions, and utilities used across modules. Reduces duplication and ensures consistency.
- `types.py` — Shared type definitions
- `exceptions.py` — Custom exception classes
- `utils.py` — Utility functions

---

### `docs/` — Documentation

**Why:** Captures the reasoning behind decisions and the evolution of the system. Essential for maintaining architectural integrity.

- `vision.md` — Product philosophy and long-term vision
- `architecture.md` — Technical architecture and design principles
- `roadmap.md` — Evolution strategy and milestone planning
- `decisions/` — Architecture Decision Records (ADRs)

---

### `tests/` — Test Suite

**Why:** Ensures system reliability as complexity grows. Protects against regression during rapid iteration.

---

### `data/` — Data Storage

**Why:** Separation of data from code enables clean development workflows and easy data management.

- `raw/` — Original uploaded files
- `transcripts/` — Transcribed text files
- `artifacts/` — Generated knowledge artifacts

---

### `scripts/` — Operational Scripts

**Why:** Automates common operational tasks without requiring full application context.

- `init_db.py` — Database initialization and migrations
- `reindex.py` — Rebuild search indices

---

### Root Files

- `docker-compose.yml` — Container orchestration for local development
- `.env.example` — Template for environment configuration
- `LICENSE` — Usage rights and restrictions

---

## Roadmap

### MVP v0.1 — Voice → Artifact
Capture voice, transcribe, reconstruct, and store as structured knowledge.

### v0.2 — Artifact → Connected Memory
Link artifacts semantically. Enable retrieval and cross-reference.

### v0.3 — Cross-time Idea Linking
Connect ideas across sessions. Surface latent patterns.

### v0.4 — Research Workspace
Dedicated environment for deep work and knowledge synthesis.

### v1.0 — Personal Cognitive Operating System
Complete system for thought capture, organization, and retrieval.

---

## Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run `docker-compose up` to start services
4. Run `python scripts/init_db.py` to initialize the database

---

## License

See [LICENSE](LICENSE) for details.