from __future__ import annotations

import shutil
import subprocess
import tomllib
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FISH = shutil.which("fish")
LUAC = shutil.which("luac") or shutil.which("luac5.4")


def repository_files(suffix: str) -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        check=True,
    )
    files: list[Path] = []
    for encoded_path in result.stdout.split(b"\0"):
        if not encoded_path:
            continue
        relative_path = Path(encoded_path.decode("utf-8"))
        if relative_path.suffix != suffix:
            continue
        candidate = REPOSITORY_ROOT
        safe = True
        for part in relative_path.parts:
            candidate /= part
            if candidate.is_symlink():
                safe = False
                break
        if safe and candidate.is_file():
            files.append(candidate)
    return files


class ReferenceSyntaxTests(unittest.TestCase):
    def test_all_repository_toml_has_valid_syntax(self) -> None:
        for path in repository_files(".toml"):
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                with path.open("rb") as document:
                    tomllib.load(document)

    @unittest.skipUnless(FISH, "Fish is required for executable module validation")
    def test_all_repository_fish_has_valid_syntax(self) -> None:
        for path in repository_files(".fish"):
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                result = subprocess.run(
                    [FISH, "--no-config", "--no-execute", path],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)

    @unittest.skipUnless(LUAC, "Lua compiler is required for syntax validation")
    def test_all_repository_lua_has_valid_syntax(self) -> None:
        for path in repository_files(".lua"):
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                result = subprocess.run(
                    [LUAC, "-p", path],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
