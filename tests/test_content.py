import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_validation_passes_for_local_demo() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_content.py", "--allow-placeholder-admin"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_single_admin_metadata_exists() -> None:
    assert (ROOT / "data" / "admin.yml").is_file()
