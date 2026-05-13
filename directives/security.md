# Security & Best Practices Directive

## Secrets Management
- Never hardcode API keys, tokens, or passwords in scripts
- Always read credentials from environment variables
- Never commit `.env` or credential files to version control
- Use `.env.example` as a template for required variables

## Code Quality
- Generated scripts must include error handling (try/except)
- Always validate user inputs before processing
- Use pathlib for file operations (cross-platform safe)
- Set explicit timeouts on all network calls

## Data Handling
- Store temporary files in `.tmp/` directory
- Clean up temporary files after processing
- Never process untrusted input without validation
- Log errors but avoid logging sensitive data
