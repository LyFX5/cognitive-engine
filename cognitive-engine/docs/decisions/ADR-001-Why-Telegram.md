# ADR-001: Why Telegram?

**Date:** 2024-01-01  
**Status:** Accepted  
**Authors:** Cognitive Engine Team

## Context

We need a user interface for capturing voice messages and receiving reconstructed artifacts. The interface must be:
- Frictionless for users
- Capable of handling voice messages
- Available on all platforms (mobile, desktop, web)
- Easy to integrate with our backend

## Options Considered

### Option 1: Custom Mobile App
Build native iOS and Android applications.

**Pros:**
- Complete control over UX
- Can leverage native voice recording features
- No third-party dependency

**Cons:**
- High development cost (2+ platforms)
- App store approval process
- User acquisition friction (download, install, register)
- Ongoing maintenance burden

### Option 2: Web Application
Build a progressive web app (PWA).

**Pros:**
- Single codebase
- No app store required
- Easy to iterate

**Cons:**
- Browser permissions for microphone can be clunky
- Background processing limitations
- Push notification complexity
- Less seamless than native apps

### Option 3: Telegram Bot
Leverage Telegram's Bot API.

**Pros:**
- Zero installation friction (users already have Telegram)
- Built-in voice message support
- Cross-platform by default
- Simple authentication (Telegram user ID)
- Mature, well-documented API
- Async communication model fits our pipeline
- No infrastructure for real-time connections

**Cons:**
- Dependency on Telegram platform
- Limited UI customization
- Telegram rate limits
- Privacy concerns for some users

### Option 4: WhatsApp Bot
Use WhatsApp Business API.

**Pros:**
- Larger user base in some regions
- Voice message support

**Cons:**
- More complex API
- Business verification required
- Less developer-friendly than Telegram
- Meta dependency (privacy concerns amplified)

## Decision

**We chose Telegram Bot.**

## Rationale

### 1. Frictionless Onboarding
Users can start using Cognitive Engine in seconds:
1. Find bot username
2. Click Start
3. Send voice message

No download, no registration form, no email verification.

### 2. Voice-First Design
Telegram was built for messaging. Voice messages are first-class citizens:
- Native recording in the app
- Automatic upload and delivery
- Playback controls for review
- Works offline (queues when connection returns)

### 3. Development Velocity
With Telegram, we focus on our core value (cognitive reconstruction), not:
- Building chat infrastructure
- Managing WebSocket connections
- Handling push notifications
- Cross-platform compatibility

### 4. Natural Interaction Model
Speaking to a bot feels appropriate. Users already:
- Send voice messages to contacts
- Use bots for various tasks
- Expect async responses

### 5. Future Flexibility
Telegram is a starting point, not a lock-in:
- We can add web interface later
- API layer abstracts the transport
- Core pipeline is interface-agnostic

## Addressing Concerns

### Privacy
Some users may hesitate to share thoughts via Telegram.

**Mitigation:**
- End-to-end encryption for data in transit
- Option for self-hosted deployment in future
- Clear privacy policy
- No data shared with Telegram beyond what's necessary

### Platform Dependency
Telegram could change APIs or policies.

**Mitigation:**
- Abstract bot interface in code
- Monitor Telegram developer communications
- Maintain ability to switch platforms if needed

### Limitations
Telegram has file size limits, rate limits, etc.

**Mitigation:**
- Design within constraints (voice messages are typically small)
- Implement retry logic
- Queue system for burst handling

## Consequences

### Positive
- Faster time to market
- Lower development cost
- Simpler architecture
- Better user onboarding

### Negative
- Less control over UI
- Platform dependency
- Some users may prefer alternatives

### Neutral
- Need to learn Telegram Bot API
- Must handle Telegram-specific edge cases

## Success Metrics

- Time from user discovery to first voice message < 2 minutes
- Voice message delivery success rate > 99%
- User reports of "easy to use" > 80%

## Review Date

This decision will be reviewed in Q2 2024 or when:
- Telegram makes breaking API changes
- User demand for alternative interfaces exceeds 20%
- We reach scale where platform risk becomes critical

---

*"The best interface is no interface."* — Golden Krishna