---
status: accepted
---

# Keep consumer configurations independently owned

A Consumer Configuration remains outside the repository's ownership and has no synchronization relationship with upstream. User intent and the Review Cursor stay beside the consumer's configuration where possible, with ignored clone-local state as a fallback, so an AI can retain context without turning the knowledge base into a stateful configuration manager.
