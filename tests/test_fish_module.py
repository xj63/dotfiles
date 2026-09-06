from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
FISH = shutil.which("fish")


class FishModuleTests(unittest.TestCase):
    def test_human_entry_point_and_agent_workflow_are_complete(self) -> None:
        readme = (REPOSITORY_ROOT / "README.md").read_text()
        guidance = (REPOSITORY_ROOT / "AGENTS.md").read_text()

        self.assertIn("Configuration Knowledge Base", readme)
        self.assertIn("Do not copy the reference unchanged", readme)
        self.assertIn("Copyable prompt", readme)
        for step in (
            "Understand the goal",
            "Inspect the existing configuration and environment",
            "Read the relevant Application Module",
            "Present a plan and impact",
            "Obtain confirmation",
            "Establish a Recovery Path and modify",
            "Validate",
            "Preserve user intent and the Review Cursor",
        ):
            self.assertIn(step, guidance)
        self.assertIn("fish/README.md", guidance)

    def test_fish_readme_covers_the_applicable_module_contract(self) -> None:
        readme = (REPOSITORY_ROOT / "fish" / "README.md").read_text()

        for heading in (
            "## Purpose",
            "## Applicable environment",
            "## Prerequisites and installation",
            "## Target configuration location",
            "## Included capabilities",
            "## Maintainer Preferences",
            "## Known conflicts",
            "## Safe validation",
            "## Consumer AI workflow",
        ):
            self.assertIn(heading, readme)
        self.assertIn("$XDG_CONFIG_HOME/fish/config.fish", readme)
        self.assertIn("https://fishshell.com/", readme)
        self.assertIn("AI-INTENT.md", readme)

    @unittest.skipUnless(FISH, "Fish is required for executable module validation")
    def test_reference_configuration_has_valid_fish_syntax(self) -> None:
        result = subprocess.run(
            [FISH, "--no-config", "--no-execute", REPOSITORY_ROOT / "fish" / "config.fish"],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)

    @unittest.skipUnless(FISH, "Fish is required for executable module validation")
    def test_optional_git_capability_is_conditioned_on_the_dependency(self) -> None:
        configuration = REPOSITORY_ROOT / "fish" / "config.fish"
        with tempfile.TemporaryDirectory() as directory:
            environment = os.environ.copy()
            environment["PATH"] = directory
            environment["TERM"] = "xterm-256color"
            without_git = subprocess.run(
                [FISH, "--no-config", "--interactive", "--command", f"source {configuration}; abbr --show gst"],
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            fake_git = Path(directory) / "git"
            fake_git.symlink_to("/usr/bin/true")
            with_git = subprocess.run(
                [FISH, "--no-config", "--interactive", "--command", f"source {configuration}; abbr --show gst"],
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertEqual("", without_git.stdout.strip())
        self.assertIn("git status --short --branch", with_git.stdout)

if __name__ == "__main__":
    unittest.main()
