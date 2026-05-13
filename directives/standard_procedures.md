# Standard Operating Procedures

## Task Approach
1. **Analyze** — Understand the user's request. Break it into discrete steps.
2. **Plan** — Determine which tools and approaches are needed.
3. **Execute** — Write and run Python scripts for ALL computational work.
4. **Verify** — Check outputs, handle errors, auto-correct if needed.
5. **Report** — Summarize what was done and the results achieved.

## Code Generation Standards
- Every script must have complete imports at the top
- Use `pathlib.Path` for file operations
- Use `subprocess.run` with `capture_output=True, text=True` for shell commands
- Set explicit `timeout` on all network and subprocess calls
- Handle errors with try/except and print meaningful error messages
- Use `argparse` or `sys.argv` for scripts that need arguments

## Script Execution Protocol
1. Write the script to `.tmp/` with a descriptive filename
2. Execute with `sys.executable` for isolation
3. Capture stdout and stderr
4. If exit code != 0, parse the traceback and auto-correct
5. Maximum 3 correction attempts before escalating

## File Management
- Deliverables go in the workspace directory (user's current directory)
- Temporary/intermediate data goes in `.tmp/`
- Never write secrets or credentials to disk
- Clean up temporary files when done
