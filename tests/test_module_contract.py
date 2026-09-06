from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECK = REPOSITORY_ROOT / "scripts" / "check"


class ApplicationModuleContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.repository = Path(self.temp_directory.name)
        subprocess.run(["git", "init", "--quiet", str(self.repository)], check=True)

    def test_discovers_a_conforming_second_module_without_fixed_sections(self) -> None:
        self.write_conforming_module()

        result = self.check("all")

        self.assertEqual(0, result.returncode, result.stdout)

    def test_reports_missing_target_location_guidance(self) -> None:
        self.write_conforming_module()
        self.write(
            "nova/README.md",
            "# Nova\n\nNova requires Nova 2. Validate safely with `nova --check`.\n",
        )

        result = self.check("all")

        self.assert_failure(result, "module.target-guidance", "nova/README.md")

    def test_reports_missing_prerequisite_guidance(self) -> None:
        self.write_conforming_module()
        self.write(
            "nova/README.md",
            "# Nova\n\nPlace `settings.toml` at `$XDG_CONFIG_HOME/nova/settings.toml`. "
            "Validate safely with `nova --check`.\n",
        )

        result = self.check("all")

        self.assert_failure(result, "module.prerequisite-guidance", "nova/README.md")

    def test_reports_missing_validation_guidance(self) -> None:
        self.write_conforming_module()
        self.write(
            "nova/README.md",
            "# Nova\n\nNova requires Nova 2. Place `settings.toml` at "
            "`$XDG_CONFIG_HOME/nova/settings.toml`.\n",
        )

        result = self.check("all")

        self.assert_failure(result, "module.validation-guidance", "nova/README.md")

    def test_existing_privacy_rules_apply_to_discovered_modules(self) -> None:
        self.write_conforming_module()
        private_path = "/Users/" + "fixture-user/.config/nova/settings.toml"
        readme = (self.repository / "nova/README.md").read_text()
        self.write("nova/README.md", readme.replace("$XDG_CONFIG_HOME/nova/settings.toml", private_path))

        result = self.check("all")

        self.assert_failure(result, "privacy.home-path", "nova/README.md")

    def test_translation_must_point_to_the_normative_english_readme(self) -> None:
        self.write_conforming_module()
        self.write("nova/README.zh-CN.md", "# Nova 中文说明\n\n这是另一份完整配置说明。\n")

        result = self.check("all")

        self.assert_failure(result, "module.translation-source", "nova/README.zh-CN.md")

    def test_staged_module_change_requires_categorized_change_information(self) -> None:
        self.write_conforming_module()
        self.write("CHANGELOG.md", "# Changelog\n\n## [Unreleased]\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("baseline")
        self.write("nova/settings.toml", "# Reusable Rule: enable focus mode.\nfocus = true\n")
        subprocess.run(["git", "add", "nova/settings.toml"], cwd=self.repository, check=True)

        missing = self.check("staged")

        self.assert_failure(missing, "module.change-information", "nova/settings.toml")

        self.write(
            "CHANGELOG.md",
            "# Changelog\n\n## [Unreleased]\n\n"
            "- **Nova / behavior**: Enable focus mode. Existing users may keep it disabled.\n",
        )
        subprocess.run(["git", "add", "CHANGELOG.md"], cwd=self.repository, check=True)

        documented = self.check("staged")

        self.assertEqual(0, documented.returncode, documented.stdout)

    def test_staged_module_removal_requires_change_information(self) -> None:
        self.write_conforming_module()
        self.write("CHANGELOG.md", "# Changelog\n\n## [Unreleased]\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("baseline")
        (self.repository / "nova/settings.toml").unlink()
        (self.repository / "nova/README.md").unlink()
        subprocess.run(["git", "add", "-A"], cwd=self.repository, check=True)

        result = self.check("staged")

        self.assert_failure(result, "module.change-information", "nova/")

    def test_full_check_uses_origin_main_for_committed_change_information(self) -> None:
        self.write_conforming_module()
        self.write("CHANGELOG.md", "# Changelog\n\n## [Unreleased]\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("baseline")
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/main", "HEAD"],
            cwd=self.repository,
            check=True,
        )
        self.write("nova/settings.toml", "# Reusable Rule: focus.\nfocus = true\n")
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        self.commit("undocumented behavior")

        result = self.check("all")

        self.assert_failure(result, "module.change-information", "nova/settings.toml")

    def write_conforming_module(self) -> None:
        self.write(
            "nova/README.md",
            "# Nova\n\n"
            "Nova requires Nova 2; install it from the official Nova site. "
            "Place `settings.toml` at `$XDG_CONFIG_HOME/nova/settings.toml`. "
            "It enables focus mode as a Maintainer Preference. "
            "Validate safely with `nova --check settings.toml`.\n",
        )
        self.write(
            "nova/settings.toml",
            "# Maintainer Preference: enable focus mode when fewer distractions are desired.\n"
            "focus = false\n",
        )

    def write(self, relative_path: str, content: str) -> None:
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def check(self, mode: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(CHECK), mode, "--root", str(self.repository)],
            text=True,
            capture_output=True,
            check=False,
        )

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

    def assert_failure(
        self,
        result: subprocess.CompletedProcess[str],
        rule: str,
        path: str,
    ) -> None:
        self.assertNotEqual(0, result.returncode)
        self.assertIn(f"BLOCKING [{rule}]", result.stdout)
        self.assertIn(path, result.stdout)


if __name__ == "__main__":
    unittest.main()
