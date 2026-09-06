from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
UPDATE_CONTEXT = REPOSITORY_ROOT / "scripts" / "update-context"
FISH = shutil.which("fish")


class UpdateContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.repository = Path(self.temp_directory.name) / "upstream"
        subprocess.run(["git", "init", "--quiet", str(self.repository)], check=True)
        self.write("CHANGELOG.md", "# Changelog\n\n## [Unreleased]\n\n### Changed\n")
        self.write("docs/local-consumer-state.md", "# Local consumer state\n")
        self.write("fish/README.md", "# Fish\n")
        self.write("fish/config.fish", "set --global fish_greeting\n")
        self.write("wezterm/README.md", "# WezTerm\n")
        self.write("wezterm/wezterm.lua", "return {}\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("baseline")
        self.cursor = self.git("rev-parse", "HEAD").strip()

    def test_filters_change_information_and_diff_to_fish(self) -> None:
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n"
            "- **Fish / behavior**: Change greeting behavior. Users must confirm before adopting it.\n"
            "- **WezTerm / appearance**: Change the color scheme. Existing users may keep theirs.\n"
            "- **Fish / Maintainer Preference**: Add a `gco` abbreviation. Existing users may decline it.\n",
        )
        self.write("fish/config.fish", "set --global fish_greeting\n# fish-diff-marker\n")
        self.write("wezterm/wezterm.lua", "-- wezterm-diff-marker\nreturn {}\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("upstream changes")

        result = self.run_context("fish")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Fish / behavior", result.stdout)
        self.assertIn("Fish / Maintainer Preference", result.stdout)
        self.assertIn("fish-diff-marker", result.stdout)
        self.assertNotIn("WezTerm / appearance", result.stdout)
        self.assertNotIn("wezterm-diff-marker", result.stdout)

    def test_reading_update_context_does_not_modify_consumer_or_cursor(self) -> None:
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n"
            "- **Fish / behavior**: Change greeting behavior. Users may decline it with no migration.\n",
        )
        self.write("fish/config.fish", "set --global fish_greeting\n# changed upstream\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("Fish update")
        consumer = Path(self.temp_directory.name) / "consumer" / "config.fish"
        consumer.parent.mkdir()
        consumer.write_text("set -gx EDITOR vi\n")
        intent = consumer.parent / "AI-INTENT.md"
        intent.write_text(f"Review Cursor: {self.cursor}\n")
        before = self.digest(consumer), self.digest(intent)

        result = self.run_context("fish")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, (self.digest(consumer), self.digest(intent)))
        self.assertIn(self.cursor, intent.read_text())

    def test_reports_missing_fish_change_information(self) -> None:
        self.write("fish/config.fish", "set --global fish_greeting\n# undocumented change\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("undocumented Fish update")

        result = self.run_context("fish")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Fish change information", result.stderr)

    def test_rejects_a_review_cursor_from_divergent_history(self) -> None:
        self.write("fish/config.fish", "set --global fish_greeting\n# cursor branch\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("cursor branch")
        divergent_cursor = self.git("rev-parse", "HEAD").strip()
        subprocess.run(
            ["git", "checkout", "--quiet", "-b", "target", self.cursor],
            cwd=self.repository,
            check=True,
        )
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n"
            "- **Fish / behavior**: Change greeting behavior. Existing users must review it.\n",
        )
        self.write("fish/config.fish", "set --global fish_greeting\n# target branch\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("target branch")
        self.cursor = divergent_cursor

        result = self.run_context("fish")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("not an ancestor", result.stderr)
        self.assertNotIn("=== REVIEW RANGE ===", result.stdout)

    def test_rejects_a_target_older_than_the_review_cursor(self) -> None:
        older_target = self.cursor
        self.write("fish/config.fish", "set --global fish_greeting\n# newer cursor\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("newer cursor")
        newer_cursor = self.git("rev-parse", "HEAD").strip()

        result = subprocess.run(
            [
                str(UPDATE_CONTEXT),
                newer_cursor,
                "fish",
                "--to",
                older_target,
                "--root",
                str(self.repository),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("not an ancestor", result.stderr)

    def test_includes_shared_consumer_protocol_changes_without_a_fish_entry(self) -> None:
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n"
            "- **repository / consumer protocol**: Clarify confirmation. Existing users need no migration.\n",
        )
        self.write("AGENTS.md", "# Agent guidance\n\nshared-protocol-marker\n")
        self.write(
            "docs/local-consumer-state.md",
            "# Local consumer state\n\nlocal-state-protocol-marker\n",
        )
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("shared protocol update")

        result = self.run_context("fish")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("repository / consumer protocol", result.stdout)
        self.assertIn("shared-protocol-marker", result.stdout)
        self.assertIn("local-state-protocol-marker", result.stdout)

    def test_rejects_an_undocumented_shared_consumer_protocol_change(self) -> None:
        self.write("AGENTS.md", "# Agent guidance\n\nundocumented-shared-marker\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("undocumented shared protocol")

        result = self.run_context("fish")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("repository / consumer protocol", result.stderr)

    def test_fish_entry_does_not_hide_an_undocumented_shared_change(self) -> None:
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n"
            "- **Fish / behavior**: Change greeting behavior. Existing users must review it.\n",
        )
        self.write("fish/config.fish", "set --global fish_greeting\n# documented Fish change\n")
        self.write("AGENTS.md", "# Agent guidance\n\nundocumented-shared-marker\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("mixed documentation coverage")

        result = self.run_context("fish")

        self.assertNotEqual(0, result.returncode)
        self.assertIn("repository / consumer protocol", result.stderr)

    def test_reports_a_module_removed_after_the_review_cursor(self) -> None:
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n### Removed\n\n"
            "- **Fish / module**: Remove the Fish module. Existing users should retain their configuration and cursor.\n",
        )
        (self.repository / "fish" / "README.md").unlink()
        (self.repository / "fish" / "config.fish").unlink()
        subprocess.run(["git", "add", "-A"], cwd=self.repository, check=True)
        self.commit("remove Fish module")

        result = self.run_context("fish")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("State: removed at target", result.stdout)
        self.assertIn("deleted file mode", result.stdout)
        self.assertIn("retain their configuration", result.stdout)

    @unittest.skipUnless(FISH, "Fish is required for partial-update acceptance")
    def test_partial_acceptance_preserves_declined_behavior_and_advances_cursor(self) -> None:
        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n### Changed\n\n"
            "- **Fish / behavior**: Offer a quiet greeting. Existing users must confirm this behavior.\n"
            "- **Fish / Maintainer Preference**: Offer a `gst` abbreviation. Existing users may decline it.\n"
            "- **WezTerm / appearance**: Change the color scheme. Fish users are unaffected.\n",
        )
        self.write(
            "fish/config.fish",
            "set --global fish_greeting\nabbr --add --global gst 'git status --short --branch'\n",
        )
        self.write("wezterm/wezterm.lua", "-- unrelated update\nreturn {}\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("mixed upstream update")
        reviewed_target = self.git("rev-parse", "HEAD").strip()
        context = self.run_context("fish")
        self.assertIn("quiet greeting", context.stdout)
        self.assertIn("`gst` abbreviation", context.stdout)
        self.assertNotIn("WezTerm / appearance", context.stdout)

        consumer = Path(self.temp_directory.name) / "consumer" / "config.fish"
        consumer.parent.mkdir()
        consumer.write_text(
            "set -gx EDITOR vi\n\n"
            "# User intent: start interactive Fish without the greeting.\n"
            "if status is-interactive\n"
            "    set --global fish_greeting\n"
            "end\n"
        )
        intent = consumer.parent / "AI-INTENT.md"
        intent.write_text(
            "Goal: keep a quiet greeting and retain explicit Git commands.\n"
            "Reason: startup focus matters; the gst preference was declined.\n"
            f"Review Cursor: {reviewed_target}\n"
        )

        validation = subprocess.run(
            [FISH, "--no-config", "--no-execute", str(consumer)],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, validation.returncode, validation.stderr)
        self.assertIn("set -gx EDITOR vi", consumer.read_text())
        self.assertNotIn("gst", consumer.read_text())
        self.assertIn("gst preference was declined", intent.read_text())
        self.assertIn(reviewed_target, intent.read_text())

    def test_agent_guidance_defines_non_synchronizing_update_decisions(self) -> None:
        guidance = (REPOSITORY_ROOT / "AGENTS.md").read_text()
        fish = (REPOSITORY_ROOT / "fish" / "README.md").read_text()

        for expected in (
            "scripts/update-context <Review-Cursor> fish",
            "focused impact report",
            "Consumer Configuration and Review Cursor unchanged",
            "only the accepted changes",
            "advance the Review Cursor",
        ):
            self.assertIn(expected, guidance + fish)
        self.assertIn("must not copy", guidance + fish)
        self.assertIn("behavior, dependency, or Maintainer Preference", guidance + fish)

    def run_context(self, application: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(UPDATE_CONTEXT), self.cursor, application, "--root", str(self.repository)],
            text=True,
            capture_output=True,
            check=False,
        )

    def write(self, relative_path: str, content: str) -> None:
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def commit(self, message: str) -> None:
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
            cwd=self.repository,
            check=True,
        )

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=True,
        ).stdout

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    unittest.main()
