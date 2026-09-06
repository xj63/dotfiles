from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
AI_REVIEW = REPOSITORY_ROOT / "scripts" / "ai-review"
AI_REVIEW_EVALUATOR = REPOSITORY_ROOT / "scripts" / "evaluate-ai-review"


class AiReviewTests(unittest.TestCase):
    def test_deterministic_failure_prevents_provider_invocation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.email", "tests@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Tests"],
                cwd=root,
                check=True,
            )

            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "check").write_bytes((REPOSITORY_ROOT / "scripts" / "check").read_bytes())
            (root / "unsafe.conf").write_text(
                "token = github_pat_" + "abcdefghijklmnopqrstuvwxyz123456\n"
            )
            marker = root / "provider-was-called"
            provider = root / "fake-provider.py"
            provider.write_text(
                "from pathlib import Path\n"
                f"Path({str(marker)!r}).write_text('called')\n"
                f"print({json.dumps(json.dumps({'blocking': [], 'advisory': []}))!r})\n"
            )

            environment = os.environ.copy()
            environment["AI_REVIEW_COMMAND"] = f"{sys.executable} {provider}"
            result = subprocess.run(
                [AI_REVIEW, "audit", "--root", root],
                cwd=root,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertIn("secret.github-token", result.stdout)
            self.assertFalse(marker.exists())

    def test_clean_audit_sends_versioned_tracked_input_to_replaceable_provider(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "user.email", "tests@example.com"],
                cwd=root,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Tests"],
                cwd=root,
                check=True,
            )
            scripts = root / "scripts"
            scripts.mkdir()
            (scripts / "check").write_bytes((REPOSITORY_ROOT / "scripts" / "check").read_bytes())
            (root / "REVIEW.md").write_text("# Test review policy\n")
            module = root / "fish"
            module.mkdir()
            (module / "README.md").write_text("# Fish\n\nPortable shell behavior.\n")
            (module / "config.fish").write_text("set -g fish_greeting\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            (module / "config.fish").write_text("set -g fish_greeting changed\n")

            captured = root.parent / f"{root.name}-provider-input.json"
            provider = root.parent / f"{root.name}-provider.py"
            provider.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                f"Path({str(captured)!r}).write_text(sys.stdin.read())\n"
                "print(json.dumps({'blocking': [], 'advisory': []}))\n"
            )
            self.addCleanup(provider.unlink, missing_ok=True)
            self.addCleanup(captured.unlink, missing_ok=True)

            environment = os.environ.copy()
            environment["AI_REVIEW_COMMAND"] = f"{sys.executable} {provider}"
            result = subprocess.run(
                [AI_REVIEW, "audit", "--root", root],
                cwd=root,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(captured.read_text())
            self.assertEqual("1", payload["contract_version"])
            self.assertEqual("audit", payload["mode"])
            self.assertEqual("# Test review policy\n", payload["policy"])
            self.assertIn("fish/config.fish", payload["repository_content"])
            self.assertIn("set -g fish_greeting changed", payload["repository_content"])

    def test_pr_review_sends_only_diff_policy_and_relevant_module_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "tests@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Tests"], cwd=root, check=True)
            (root / "scripts").mkdir()
            (root / "scripts" / "check").write_bytes(
                (REPOSITORY_ROOT / "scripts" / "check").read_bytes()
            )
            (root / ".gitignore").write_text("/.local/\n*.bak\n")
            (root / "REVIEW.md").write_text("# Policy from the reviewed commit\n")
            for name in ("fish", "zed"):
                (root / name).mkdir()
                (root / name / "README.md").write_text(f"# {name.title()} module context\n")
            (root / "fish" / "config.fish").write_text("set -g fish_greeting hello\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
            base = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, capture_output=True
            ).stdout.strip()

            (root / "fish" / "config.fish").write_text("set -g fish_greeting\n")
            external = root.parent / f"{root.name}-external-config"
            external.write_text("PRIVATE USER CONFIG CONTENT\n")
            self.addCleanup(external.unlink, missing_ok=True)
            (root / "fish" / "external-link").symlink_to(external)
            subprocess.run(["git", "add", "fish"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "change fish"], cwd=root, check=True)
            head = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, capture_output=True
            ).stdout.strip()
            (root / ".local").mkdir()
            (root / ".local" / "intent.md").write_text("IGNORED LOCAL INTENT\n")
            (root / "notes.bak").write_text("IGNORED BACKUP CONTENT\n")

            captured = root.parent / f"{root.name}-pr-input.json"
            provider = root.parent / f"{root.name}-pr-provider.py"
            provider.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                f"Path({str(captured)!r}).write_text(sys.stdin.read())\n"
                "print(json.dumps({'blocking': [], 'advisory': []}))\n"
            )
            self.addCleanup(provider.unlink, missing_ok=True)
            self.addCleanup(captured.unlink, missing_ok=True)
            environment = os.environ.copy()
            environment["AI_REVIEW_COMMAND"] = f"{sys.executable} {provider}"

            result = subprocess.run(
                [AI_REVIEW, "pr", "--root", root, "--base", base, "--head", head],
                cwd=root,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(captured.read_text())
            serialized = json.dumps(payload)
            self.assertEqual("pr", payload["mode"])
            self.assertIn("fish/config.fish", payload["diff"])
            self.assertIn("fish/external-link", payload["diff"])
            self.assertEqual(
                [{"path": "fish/README.md", "content": "# Fish module context\n"}],
                payload["module_context"],
            )
            self.assertNotIn("Zed module context", serialized)
            self.assertNotIn("PRIVATE USER CONFIG CONTENT", serialized)
            self.assertNotIn("IGNORED LOCAL INTENT", serialized)
            self.assertNotIn("IGNORED BACKUP CONTENT", serialized)

    def test_provider_findings_must_include_evidence_rationale_and_disposition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "tests@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Tests"], cwd=root, check=True)
            (root / "scripts").mkdir()
            (root / "scripts" / "check").write_bytes(
                (REPOSITORY_ROOT / "scripts" / "check").read_bytes()
            )
            (root / "REVIEW.md").write_text("# Policy\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)

            provider = root.parent / f"{root.name}-invalid-provider.py"
            provider.write_text(
                "import json\n"
                "print(json.dumps({'blocking': [{'path': 'fish/config.fish'}], 'advisory': []}))\n"
            )
            self.addCleanup(provider.unlink, missing_ok=True)
            environment = os.environ.copy()
            environment["AI_REVIEW_COMMAND"] = f"{sys.executable} {provider}"

            result = subprocess.run(
                [AI_REVIEW, "audit", "--root", root],
                cwd=root,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(2, result.returncode)
            self.assertIn("invalid finding", result.stderr.lower())

    def test_provider_failure_does_not_echo_private_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "tests@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Tests"], cwd=root, check=True)
            (root / "scripts").mkdir()
            (root / "scripts" / "check").write_bytes(
                (REPOSITORY_ROOT / "scripts" / "check").read_bytes()
            )
            (root / "REVIEW.md").write_text("# Policy\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            provider = root.parent / f"{root.name}-failing-provider.py"
            provider.write_text(
                "import sys\n"
                "print('private-provider-diagnostic', file=sys.stderr)\n"
                "raise SystemExit(1)\n"
            )
            self.addCleanup(provider.unlink, missing_ok=True)
            environment = os.environ.copy()
            environment["AI_REVIEW_COMMAND"] = f"{sys.executable} {provider}"

            result = subprocess.run(
                [AI_REVIEW, "audit", "--root", root],
                cwd=root,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(2, result.returncode)
            self.assertNotIn("private-provider-diagnostic", result.stdout + result.stderr)
            self.assertIn("provider failed", result.stderr.lower())

    def test_openai_adapter_disables_storage_and_requests_strict_schema(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "tests@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Tests"], cwd=root, check=True)
            (root / "scripts").mkdir()
            (root / "scripts" / "check").write_bytes(
                (REPOSITORY_ROOT / "scripts" / "check").read_bytes()
            )
            (root / "REVIEW.md").write_text("# Policy\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)

            capture = root.parent / f"{root.name}-openai-request.json"
            port_file = root.parent / f"{root.name}-openai-port"
            server_script = root.parent / f"{root.name}-openai-server.py"
            server_script.write_text(
                "import json\n"
                "import socketserver\n"
                "from http.server import BaseHTTPRequestHandler, HTTPServer\n"
                "from pathlib import Path\n"
                f"capture = Path({str(capture)!r})\n"
                f"port_file = Path({str(port_file)!r})\n"
                "class Handler(BaseHTTPRequestHandler):\n"
                "    def do_POST(self):\n"
                "        length = int(self.headers['Content-Length'])\n"
                "        capture.write_text(json.dumps({\n"
                "            'headers': dict(self.headers),\n"
                "            'body': json.loads(self.rfile.read(length)),\n"
                "        }))\n"
                "        review = json.dumps({'blocking': [], 'advisory': []})\n"
                "        response = json.dumps({'output': [{'type': 'message', 'content': [\n"
                "            {'type': 'output_text', 'text': review}\n"
                "        ]}]}).encode()\n"
                "        self.send_response(200)\n"
                "        self.send_header('Content-Type', 'application/json')\n"
                "        self.send_header('Content-Length', str(len(response)))\n"
                "        self.end_headers()\n"
                "        self.wfile.write(response)\n"
                "    def log_message(self, format, *args):\n"
                "        pass\n"
                "class LocalHTTPServer(HTTPServer):\n"
                "    def server_bind(self):\n"
                "        socketserver.TCPServer.server_bind(self)\n"
                "        self.server_name = 'localhost'\n"
                "        self.server_port = self.socket.getsockname()[1]\n"
                "server = LocalHTTPServer(('127.0.0.1', 0), Handler)\n"
                "port_file.write_text(str(server.server_port))\n"
                "server.handle_request()\n"
            )
            server = subprocess.Popen(
                [sys.executable, server_script], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            def stop_server() -> None:
                if server.poll() is None:
                    server.kill()
                server.communicate()
            self.addCleanup(stop_server)
            for _ in range(500):
                if port_file.exists():
                    break
                time.sleep(0.01)
            if not port_file.exists():
                server.kill()
                _, server_error = server.communicate()
                self.fail(f"test HTTP server did not start: {server_error}")
            for path in (capture, port_file, server_script):
                self.addCleanup(path.unlink, missing_ok=True)

            environment = os.environ.copy()
            environment.pop("AI_REVIEW_COMMAND", None)
            environment["OPENAI_API_KEY"] = "test-placeholder-value"
            environment["OPENAI_RESPONSES_URL"] = (
                f"http://127.0.0.1:{port_file.read_text()}/v1/responses"
            )
            result = subprocess.run(
                [AI_REVIEW, "audit", "--root", root],
                cwd=root,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            server.communicate(timeout=5)

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            captured_request = json.loads(capture.read_text())
            headers = captured_request["headers"]
            request = captured_request["body"]
            self.assertEqual("Bearer test-placeholder-value", headers["Authorization"])
            self.assertFalse(request["store"])
            self.assertTrue(request["text"]["format"]["strict"])
            self.assertEqual("json_schema", request["text"]["format"]["type"])
            self.assertNotIn("test-placeholder-value", request["input"])

    def test_only_blocking_findings_fail_the_review_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "tests@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Tests"], cwd=root, check=True)
            (root / "scripts").mkdir()
            (root / "scripts" / "check").write_bytes(
                (REPOSITORY_ROOT / "scripts" / "check").read_bytes()
            )
            (root / "REVIEW.md").write_text("# Policy\n")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "fixture"], cwd=root, check=True)
            provider = root.parent / f"{root.name}-severity-provider.py"
            self.addCleanup(provider.unlink, missing_ok=True)
            environment = os.environ.copy()
            environment["AI_REVIEW_COMMAND"] = f"{sys.executable} {provider}"

            finding = {
                "path": "fish/config.fish",
                "line": 4,
                "evidence": "The changed line exposes a value.",
                "policy_rule": "privacy.contextual-identifier",
                "consequence": "A private identifier would become public.",
                "disposition": "Replace the value with a placeholder.",
            }
            for severity, expected_status in (("advisory", 1), ("blocking", 1)):
                response = {"blocking": [], "advisory": []}
                response[severity].append({"severity": severity, **finding})
                provider.write_text(
                    "import json\n"
                    f"print(json.dumps({response!r}))\n"
                )
                result = subprocess.run(
                    [AI_REVIEW, "audit", "--root", root],
                    cwd=root,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                with self.subTest(severity=severity):
                    self.assertEqual(expected_status, result.returncode)
                    self.assertIn("privacy.contextual-identifier", result.stdout)
                    self.assertIn("Replace the value with a placeholder.", result.stdout)

                if severity == "advisory":
                    accepted_environment = environment.copy()
                    accepted_environment["AI_REVIEW_ADVISORY_REASON"] = (
                        "The macOS-only scope is intentional for this release."
                    )
                    accepted = subprocess.run(
                        [AI_REVIEW, "audit", "--root", root],
                        cwd=root,
                        env=accepted_environment,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(0, accepted.returncode)
                    self.assertIn("Maintainer acceptance", accepted.stdout)
                    self.assertIn("macOS-only scope", accepted.stdout)

    def test_semantic_fixture_evaluator_requires_expected_categories(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            provider = Path(directory) / "fixture-provider.py"
            provider.write_text(
                "import json, sys\n"
                "payload = json.load(sys.stdin)\n"
                "diff = payload['diff']\n"
                "blocking, advisory = [], []\n"
                "finding = {'line': 1, 'consequence': 'The change affects consumers.'}\n"
                "if \"+config.default_prog = {'ssh', 'alex-bedroom-nas'}\" in diff:\n"
                "  blocking.append({'severity': 'blocking', 'path': 'wezterm/wezterm.lua',\n"
                "    'policy_rule': 'privacy contextual identifier',\n"
                "    'evidence': 'alex-bedroom-nas identifies a private device.',\n"
                "    'disposition': 'Replace it with a public placeholder.', **finding})\n"
                "elif 'always distracting' in diff:\n"
                "  advisory.append({'severity': 'advisory', 'path': 'fish/config.fish',\n"
                "    'policy_rule': 'maintainer preference',\n"
                "    'evidence': 'The text says always distracting.',\n"
                "    'disposition': 'Qualify it as a maintainer preference.', **finding})\n"
                "elif 'fzf_configure_bindings' in diff:\n"
                "  advisory.append({'severity': 'advisory', 'path': 'fish/config.fish',\n"
                "    'policy_rule': 'missing prerequisite',\n"
                "    'evidence': 'fzf_configure_bindings is invoked.',\n"
                "    'disposition': 'Document the prerequisite and installation.', **finding})\n"
                "elif '/opt/homebrew/bin/fish' in diff:\n"
                "  advisory.append({'severity': 'advisory', 'path': 'zed/settings.json',\n"
                "    'policy_rule': 'portability',\n"
                "    'evidence': '/opt/homebrew/bin/fish is absolute.',\n"
                "    'disposition': 'Detect or document a portable substitute.', **finding})\n"
                "print(json.dumps({'blocking': blocking, 'advisory': advisory}))\n"
            )
            environment = os.environ.copy()
            environment["AI_REVIEW_COMMAND"] = f"{sys.executable} {provider}"

            result = subprocess.run(
                [AI_REVIEW_EVALUATOR],
                cwd=REPOSITORY_ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(7, result.stdout.count("PASS "))


if __name__ == "__main__":
    unittest.main()
