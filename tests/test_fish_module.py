from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


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

    def test_theme_uses_fish_native_selection_without_generated_assignments(self) -> None:
        theme = (REPOSITORY_ROOT / "fish" / "conf.d" / "theme.fish").read_text()

        self.assertIn("fish_config theme choose Nord", theme)
        self.assertNotRegex(theme, r"(?m)^\s*set\b.*\bfish_(?:pager_)?color_")

if __name__ == "__main__":
    unittest.main()
