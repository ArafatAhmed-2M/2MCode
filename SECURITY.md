# Security Policy

## Supported Versions

We currently provide security updates for the latest stable release.

| Version | Supported |
|---|---|
| Latest (1.x) | ✅ |
| Older releases | ❌ |

## Reporting a Vulnerability

If you discover a security vulnerability in 2M Code, please report it privately.

**Do not** open a public issue. Instead, send a description of the vulnerability to the repository maintainers via a private method:

1. Open a [private security advisory](https://github.com/ArafatAhmed-2M/2MCode/security/advisories/new) on GitHub
2. Or email the repository owner directly

Please include:
- Type of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if known)

We will respond within 48 hours and work to address the issue promptly.

## Disclosure Policy

- We will acknowledge receipt of your report within 48 hours
- We will provide an estimated timeline for a fix
- We will notify you when the vulnerability is fixed
- Public disclosure will happen after a fix is released

## Best Practices

- Never commit API keys or secrets to the repository
- Use `.env` for local configuration (it's in `.gitignore`)
- Run `2mcode` with appropriate permission modes when in sensitive environments
- Keep your installation up to date
