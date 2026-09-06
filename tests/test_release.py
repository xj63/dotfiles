from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RELEASE_CHECK = ROOT / "scripts" / "release-check"
UPDATE_CONTEXT = ROOT / "scripts" / "update-context"


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

    def test_release_tag_supports_fresh_and_existing_review_cursors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "upstream"
            subprocess.run(["git", "init", "--quiet", str(repository)], check=True)
            (repository / "CHANGELOG.md").write_text("# Changelog\n\n## [Unreleased]\n")
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            self._commit(repository, "pre-module baseline")
            earlier_cursor = self._git(repository, "rev-parse", "HEAD").strip()
            fish = repository / "fish"
            fish.mkdir()
            (fish / "README.md").write_text("# Fish\n")
            (fish / "config.fish").write_text("set --global fish_greeting\n")
            (repository / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n\n## [1.0.0] - 2026-09-07\n\n"
                "### Added\n\n- **Fish / module**: Add the initial Fish module.\n"
            )
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            self._commit(repository, "release")
            subprocess.run(["git", "tag", "v1.0.0"], cwd=repository, check=True)
            consumer = Path(directory) / "consumer-config.fish"
            consumer.write_text("set -gx EDITOR vi\n")
            before = hashlib.sha256(consumer.read_bytes()).hexdigest()

            existing = subprocess.run(
                [str(UPDATE_CONTEXT), earlier_cursor, "fish", "--to", "v1.0.0", "--root", str(repository)],
                text=True,
                capture_output=True,
                check=False,
            )
            fresh = subprocess.run(
                [str(UPDATE_CONTEXT), "v1.0.0", "fish", "--to", "v1.0.0", "--root", str(repository)],
                text=True,
                capture_output=True,
                check=False,
            )
            after = hashlib.sha256(consumer.read_bytes()).hexdigest()

        self.assertEqual(0, existing.returncode, existing.stderr)
        self.assertIn("Fish / module", existing.stdout)
        self.assertEqual(0, fresh.returncode, fresh.stderr)
        self.assertIn("No application change information in this range", fresh.stdout)
        self.assertEqual(before, after)

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

    @staticmethod
    def _git(repository: Path, *arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments],
            cwd=repository,
            text=True,
            capture_output=True,
            check=True,
        ).stdout


if __name__ == "__main__":
    unittest.main()
