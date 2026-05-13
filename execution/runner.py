from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import uuid
from pathlib import Path
from typing import Optional

from core.ui import console, show_traceback

TMP_DIR = Path.cwd() / ".tmp"

# Ensure project .tmp directory exists
TMP_DIR.mkdir(parents=True, exist_ok=True)


class ScriptResult:
    def __init__(self, success: bool, output: str, error: str, exit_code: int, script_path: Path):
        self.success = success
        self.output = output
        self.error = error
        self.exit_code = exit_code
        self.script_path = script_path
        self.traceback = self._extract_traceback(error)

    @staticmethod
    def _extract_traceback(error: str) -> str:
        if "Traceback" in error:
            tb_start = error.index("Traceback")
            return error[tb_start:]
        return ""

    def __repr__(self) -> str:
        status = "SUCCESS" if self.success else "FAILED"
        return f"<ScriptResult {status} exit={self.exit_code}>"


def extract_code_blocks(text: str) -> list[dict]:
    pattern = r"```(?:python)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"language": "python", "code": m.strip()} for m in matches]


def write_script(code: str, filename: Optional[str] = None) -> Path:
    if filename is None:
        filename = f"script_{uuid.uuid4().hex[:8]}.py"
    script_path = TMP_DIR / filename
    script_path.write_text(code, encoding="utf-8")
    return script_path


def execute_script(script_path: Path, timeout: int = 120) -> ScriptResult:
    try:
        proc = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=TMP_DIR,
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
        return ScriptResult(
            success=proc.returncode == 0,
            output=proc.stdout,
            error=proc.stderr,
            exit_code=proc.returncode,
            script_path=script_path,
        )
    except subprocess.TimeoutExpired:
        return ScriptResult(
            success=False,
            output="",
            error=f"Script timed out after {timeout}s",
            exit_code=-1,
            script_path=script_path,
        )
    except Exception as e:
        return ScriptResult(
            success=False,
            output="",
            error=str(e),
            exit_code=-1,
            script_path=script_path,
        )


def run_python_code(code: str, timeout: int = 120) -> ScriptResult:
    script_path = write_script(code)
    result = execute_script(script_path, timeout)
    if not result.success:
        traceback_path = TMP_DIR / f"traceback_{script_path.stem}.log"
        traceback_path.write_text(result.error, encoding="utf-8")
    return result


def cleanup_scripts(max_age_minutes: int = 60) -> int:
    import time
    now = time.time()
    count = 0
    for f in TMP_DIR.glob("*.py"):
        if now - f.stat().st_mtime > max_age_minutes * 60:
            f.unlink()
            count += 1
    for f in TMP_DIR.glob("traceback_*.log"):
        if now - f.stat().st_mtime > max_age_minutes * 60:
            f.unlink()
            count += 1
    return count
