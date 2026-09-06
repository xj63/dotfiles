from __future__ import annotations

import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECK_COMMAND = REPOSITORY_ROOT / "scripts" / "check"


class RepositoryCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.repository = Path(self.temp_directory.name)
        subprocess.run(
            ["git", "init", "--quiet", str(self.repository)],
            check=True,
        )

    def write(self, relative_path: str, content: str) -> None:
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def run_check(self, mode: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(CHECK_COMMAND), mode, "--root", str(self.repository)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_full_check_blocks_a_known_github_token(self) -> None:
        token = "ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        self.write("fish/config.fish", f"set -gx TOKEN {token}\n")

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [secret.github-token]", result.stdout)
        self.assertIn("fish/config.fish:1", result.stdout)

    def test_staged_check_reads_the_index_instead_of_the_worktree(self) -> None:
        token = "ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        self.write("fish/config.fish", f"set -gx TOKEN {token}\n")
        subprocess.run(
            ["git", "add", "fish/config.fish"],
            cwd=self.repository,
            check=True,
        )
        self.write("fish/config.fish", "# the worktree copy is safe\n")

        result = self.run_check("staged")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [secret.github-token]", result.stdout)

    def test_full_check_blocks_a_personal_home_path(self) -> None:
        home_path = "/Users/" + "alice/bin/tool"
        self.write("zed/settings.json", f'{{"terminal": "{home_path}"}}\n')

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [privacy.home-path]", result.stdout)
        self.assertIn("zed/settings.json:1", result.stdout)

    def test_full_check_blocks_a_private_email_address(self) -> None:
        email = "alice" + "@private-mail.com"
        self.write("wezterm/wezterm.lua", f'config.author = "{email}"\n')

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [privacy.email]", result.stdout)

    def test_full_check_accepts_an_explicit_public_identity_exception(self) -> None:
        email = "maintainer" + "@public.example.dev"
        self.write("fish/config.fish", f"# Public contact: {email}\n")
        self.write(
            "review-allowlist.txt",
            f"{email}\tPublished project contact address\n",
        )

        result = self.run_check("all")

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_identity_exception_never_suppresses_a_secret(self) -> None:
        token = "ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        self.write("fish/config.fish", f"set -gx TOKEN {token}\n")
        self.write("review-allowlist.txt", f"{token}\tIncorrect secret exception\n")

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [secret.github-token]", result.stdout)

    def test_staged_check_uses_an_unchanged_allowlist_from_the_index(self) -> None:
        email = "maintainer" + "@public.example.dev"
        self.write(
            "review-allowlist.txt",
            f"{email}\tPublished project contact address\n",
        )
        subprocess.run(["git", "add", "review-allowlist.txt"], cwd=self.repository, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=user@example.com", "commit", "--quiet", "-m", "allow identity"],
            cwd=self.repository,
            check=True,
        )
        self.write("fish/config.fish", f"# Public contact: {email}\n")
        subprocess.run(["git", "add", "fish/config.fish"], cwd=self.repository, check=True)

        result = self.run_check("staged")

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_staged_check_revalidates_repository_when_an_exception_is_removed(self) -> None:
        email = "maintainer" + "@public.example.dev"
        self.write("fish/config.fish", f"# Public contact: {email}\n")
        self.write(
            "review-allowlist.txt",
            f"{email}\tPublished project contact address\n",
        )
        subprocess.run(["git", "add", "."], cwd=self.repository, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=user@example.com", "commit", "--quiet", "-m", "allow identity"],
            cwd=self.repository,
            check=True,
        )
        (self.repository / "review-allowlist.txt").unlink()
        subprocess.run(["git", "add", "-u"], cwd=self.repository, check=True)

        result = self.run_check("staged")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [privacy.email]", result.stdout)

    def test_full_check_rejects_an_identity_exception_without_a_reason(self) -> None:
        email = "maintainer" + "@public.example.dev"
        self.write("review-allowlist.txt", f"{email}\n")

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [policy.identity-allowlist]", result.stdout)

    def test_full_check_blocks_a_private_network_address(self) -> None:
        private_address = "192.168." + "10.24"
        self.write("wezterm/wezterm.lua", f'config.ssh_host = "{private_address}"\n')

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [privacy.private-network]", result.stdout)

    def test_full_check_blocks_a_device_identifier(self) -> None:
        device_identifier = "00:1A:" + "2B:3C:4D:5E"
        self.write("tool/settings.toml", f'device = "{device_identifier}"\n')

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [privacy.device-identifier]", result.stdout)

    def test_full_check_blocks_a_private_hostname(self) -> None:
        hostname = "workstation." + "internal"
        self.write("tool/settings.toml", f'host = "{hostname}"\n')

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [privacy.private-host]", result.stdout)

    def test_full_check_blocks_a_hardcoded_generic_credential(self) -> None:
        credential = "sensitive-" + "credential-value-1234"
        self.write("tool/settings.toml", f'api_key = "{credential}"\n')

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [secret.hardcoded-credential]", result.stdout)

    def test_full_check_blocks_a_private_key(self) -> None:
        key_header = "-----BEGIN " + "PRIVATE KEY-----"
        self.write("keys/id.pem", f"{key_header}\nnot-a-real-key\n")

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [secret.private-key]", result.stdout)

    def test_full_check_blocks_invalid_json_configuration(self) -> None:
        self.write("zed/README.md", "# Zed\n")
        self.write("zed/settings.json", '{"theme": "dark",}\n')

        result = self.run_check("all")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [syntax.json] zed/settings.json:1", result.stdout)

    def test_full_check_does_not_parse_json_outside_an_application_module(self) -> None:
        self.write("tests/README.md", "# Test fixtures\n")
        self.write("tests/fixture.json", '{"intentionally": "invalid",}\n')

        result = self.run_check("all")

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_staged_check_blocks_tracked_local_consumer_state(self) -> None:
        token = "ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        self.write(".local/fish-intent.md", f"Private local value: {token}\n")
        subprocess.run(
            ["git", "add", "--force", ".local/fish-intent.md"],
            cwd=self.repository,
            check=True,
        )

        result = self.run_check("staged")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [policy.local-consumer-state]", result.stdout)
        self.assertNotIn("secret.github-token", result.stdout)

    def test_full_check_accepts_portable_placeholders_and_ignored_local_state(self) -> None:
        self.write(".gitignore", "/.local/\n")
        self.write("fish/README.md", "# Fish\n")
        self.write(
            "fish/settings.json",
            "{\n"
            '  "home": "$HOME",\n'
            '  "email": "user@example.com",\n'
            '  "host": "host.example.com",\n'
            '  "address": "192.0.2.1",\n'
            '  "device": "<device-id>",\n'
            '  "api_key": "${API_KEY}",\n'
            '  "github_token": "ghp_<token>",\n'
            '  "private_key": "<private-key>"\n'
            "}\n",
        )
        token = "ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        self.write(".local/private.md", f"Ignored local value: {token}\n")

        result = self.run_check("all")

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_full_check_does_not_follow_a_symlink_outside_the_repository(self) -> None:
        external_directory = tempfile.TemporaryDirectory()
        self.addCleanup(external_directory.cleanup)
        external_file = Path(external_directory.name) / "external.txt"
        token = "ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        external_file.write_text(token, encoding="utf-8")
        link = self.repository / "external-link"
        link.symlink_to(external_file)

        result = self.run_check("all")

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_installed_commit_hook_delegates_to_the_staged_check(self) -> None:
        for relative_path in (
            "scripts/check",
            "scripts/install-hooks",
            ".githooks/pre-commit",
        ):
            source = REPOSITORY_ROOT / relative_path
            destination = self.repository / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        subprocess.run(
            [str(self.repository / "scripts" / "install-hooks")],
            cwd=self.repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "user@example.com"],
            cwd=self.repository,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture User"],
            cwd=self.repository,
            check=True,
        )
        token = "ghp_" + "abcdefghijklmnopqrstuvwxyz1234567890"
        self.write("fish/config.fish", f"set -gx TOKEN {token}\n")
        subprocess.run(["git", "add", "fish/config.fish"], cwd=self.repository, check=True)

        result = subprocess.run(
            ["git", "commit", "-m", "unsafe fixture"],
            cwd=self.repository,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("BLOCKING [secret.github-token]", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
