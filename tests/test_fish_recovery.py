from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
REVIEW_CONTEXT = REPOSITORY_ROOT / "scripts" / "review-context"


class FishRecoveryProtocolTests(unittest.TestCase):
    def test_fish_guidance_defines_recovery_and_intent_priority(self) -> None:
        guidance = (REPOSITORY_ROOT / "fish" / "README.md").read_text()

        self.assertIn("git restore", guidance)
        self.assertIn("only the affected files", guidance)
        self.assertIn("Markdown document", guidance)
        self.assertIn("inside the Fish configuration directory", guidance)
        self.assertIn("ignored `.local/` state", guidance)
        self.assertIn("target location", guidance)
        self.assertIn("Review Cursor", guidance)
        self.assertIn("must not contain credentials", guidance)
        self.assertIn("a copy of the Consumer Configuration", guidance)

    def test_local_state_and_backups_are_ignored_by_git(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "clone"
            subprocess.run(
                ["git", "clone", "--quiet", str(REPOSITORY_ROOT), str(clone)],
                check=True,
            )
            local_intent = clone / ".local" / "fish" / "intent.md"
            backup = clone / "fish" / "config.fish.backup"
            local_intent.parent.mkdir(parents=True)
            local_intent.write_text("Private goal\n")
            backup.write_text("Private consumer configuration\n")

            status = subprocess.run(
                ["git", "status", "--short", "--untracked-files=all"],
                cwd=clone,
                text=True,
                capture_output=True,
                check=True,
            )

        self.assertEqual("", status.stdout)

    def test_review_context_contains_only_tracked_review_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            subprocess.run(["git", "init", "--quiet", str(repository)], check=True)
            subprocess.run(["git", "checkout", "-b", "main"], cwd=repository, check=True, capture_output=True)
            self._write(repository, ".gitignore", "/.local/\n*.backup\n")
            self._write(repository, "REVIEW.md", "review-policy-marker\n")
            self._write(repository, "fish/README.md", "fish-context-marker\n")
            self._write(repository, "fish/config.fish", "set fish_greeting\n")
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            self._commit(repository, "baseline")
            subprocess.run(["git", "checkout", "-b", "change"], cwd=repository, check=True, capture_output=True)
            self._write(repository, "fish/config.fish", "set fish_greeting\n# tracked-diff-marker\n")
            self._write(repository, ".local/fish/intent.md", "private-intent-marker\n")
            self._write(repository, "fish/config.fish.backup", "private-backup-marker\n")
            external = Path(directory) / "consumer-config.fish"
            external.write_text("external-consumer-marker\n")
            subprocess.run(["git", "add", "fish/config.fish"], cwd=repository, check=True)
            self._commit(repository, "change config")

            result = subprocess.run(
                [str(REVIEW_CONTEXT), "main", "--root", str(repository)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("review-policy-marker", result.stdout)
        self.assertIn("fish-context-marker", result.stdout)
        self.assertIn("tracked-diff-marker", result.stdout)
        self.assertNotIn("private-intent-marker", result.stdout)
        self.assertNotIn("private-backup-marker", result.stdout)
        self.assertNotIn("external-consumer-marker", result.stdout)

    def test_review_context_does_not_follow_a_tracked_module_readme_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            subprocess.run(["git", "init", "--quiet", str(repository)], check=True)
            subprocess.run(["git", "checkout", "-b", "main"], cwd=repository, check=True, capture_output=True)
            self._write(repository, "REVIEW.md", "review policy\n")
            external = Path(directory) / "external.md"
            external.write_text("external-private-marker\n")
            module = repository / "fish"
            module.mkdir()
            (module / "README.md").symlink_to(external)
            self._write(repository, "fish/config.fish", "set fish_greeting\n")
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            self._commit(repository, "baseline")
            subprocess.run(["git", "checkout", "-b", "change"], cwd=repository, check=True, capture_output=True)
            self._write(repository, "fish/config.fish", "set fish_greeting\n# change\n")
            subprocess.run(["git", "add", "fish/config.fish"], cwd=repository, check=True)
            self._commit(repository, "change config")

            result = subprocess.run(
                [str(REVIEW_CONTEXT), "main", "--root", str(repository)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("external-private-marker", result.stdout)

    def test_review_context_does_not_run_a_configured_textconv_filter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            subprocess.run(["git", "init", "--quiet", str(repository)], check=True)
            subprocess.run(["git", "checkout", "-b", "main"], cwd=repository, check=True, capture_output=True)
            self._write(repository, "REVIEW.md", "review policy\n")
            self._write(repository, "fish/README.md", "fish module\n")
            self._write(repository, "fish/config.fish", "set fish_greeting\n")
            self._write(repository, ".gitattributes", "fish/config.fish diff=leaky\n")
            subprocess.run(["git", "add", "."], cwd=repository, check=True)
            self._commit(repository, "baseline")

            external = Path(directory) / "external-private.txt"
            external.write_text("external-textconv-marker\n")
            helper = Path(directory) / "textconv"
            helper.write_text(f"#!/bin/sh\ncat '{external}'\ncat \"$1\"\n")
            helper.chmod(0o755)
            subprocess.run(
                ["git", "config", "diff.leaky.textconv", str(helper)],
                cwd=repository,
                check=True,
            )
            subprocess.run(["git", "checkout", "-b", "change"], cwd=repository, check=True, capture_output=True)
            self._write(repository, "fish/config.fish", "set fish_greeting\n# change\n")
            subprocess.run(["git", "add", "fish/config.fish"], cwd=repository, check=True)
            self._commit(repository, "change config")

            result = subprocess.run(
                [str(REVIEW_CONTEXT), "main", "--root", str(repository)],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("external-textconv-marker", result.stdout)

    @staticmethod
    def _write(root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

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
