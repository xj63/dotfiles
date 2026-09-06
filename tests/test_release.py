from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_CHECK = ROOT / "scripts" / "release-check"


class ReleaseTests(unittest.TestCase):
    def test_semantic_version_classification(self) -> None:
        cases = {
            "breaking-protocol": "major",
            "module-layout": "major",
            "new-module": "minor",
            "new-capability": "minor",
            "dependency": "minor",
            "behavior": "minor",
            "documentation": "patch",
            "non-behavioral-correction": "patch",
        }
        for change, expected in cases.items():
            with self.subTest(change=change):
                result = subprocess.run(
                    [str(RELEASE_CHECK), "classify", change],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(expected, result.stdout.strip())

    def test_prepared_release_has_fresh_unreleased_and_equivalent_notes(self) -> None:
        result = subprocess.run(
            [
                str(RELEASE_CHECK),
                "verify",
                "1.0.0",
                "--root",
                str(ROOT),
                "--notes",
                "docs/releases/1.0.0.md",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)

    def test_tag_required_verification_rejects_a_tag_not_at_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            subprocess.run(["git", "init", "--quiet", str(repository)], check=True)
            self._write_release_fixture(repository)
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            self._commit(repository, "release")
            subprocess.run(["git", "tag", "v1.0.0"], cwd=repository, check=True)
            (repository / "later.txt").write_text("later\n")
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            self._commit(repository, "later")

            result = subprocess.run(
                [
                    str(RELEASE_CHECK),
                    "verify",
                    "1.0.0",
                    "--root",
                    str(repository),
                    "--notes",
                    "docs/releases/1.0.0.md",
                    "--tag-required",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("v1.0.0 does not identify HEAD", result.stderr)

    @staticmethod
    def _write_release_fixture(repository: Path) -> None:
        changelog = (
            "# Changelog\n\n## [Unreleased]\n\n"
            "## [1.0.0] - 2026-09-07\n\n### Added\n\n- **Fish / module**: Initial Fish module.\n"
        )
        notes = "# 1.0.0\n\n### Added\n\n- **Fish / module**: Initial Fish module.\n"
        (repository / "CHANGELOG.md").write_text(changelog)
        path = repository / "docs/releases/1.0.0.md"
        path.parent.mkdir(parents=True)
        path.write_text(notes)

    @staticmethod
    def _commit(repository: Path, message: str) -> None:
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=user@example.com",
                "commit",
                "--quiet",
                "-m",
                message,
            ],
            cwd=repository,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
