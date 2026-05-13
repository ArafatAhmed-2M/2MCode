# Directives

Place custom operating procedures here as Markdown files.

Each `.md` file in this directory is loaded into the system prompt
as a Layer 1 Directive, instructing the Orchestrator how to handle
specific types of tasks.

## Example: security.md

```markdown
# Security Directive

When handling user credentials or API keys:
1. Never log or display secrets
2. Always read sensitive data from environment variables
3. Never commit .env files to version control
```

## Example: api_patterns.md

```markdown
# API Integration Directive

When writing API client code:
1. Always implement retry logic with exponential backoff
2. Set reasonable timeouts (default 30s)
3. Handle HTTP error codes gracefully
4. Log request IDs for debugging
```
