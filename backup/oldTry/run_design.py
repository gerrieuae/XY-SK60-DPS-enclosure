#!/usr/bin/env python3
"""
Run the 36V DC power supply enclosure design in SolidCraft via the MCP CLI.

Usage:
    python run_design.py
    python run_design.py --steps power_module_steps.json
    python run_design.py --log run.log
    python run_design.py --dry-run        # validate JSON only, no SolidCraft needed

Requires solidcraft-cli on PATH (installed with SolidCraft desktop app).
Open SolidCraft desktop app and create a new document BEFORE running this script.
"""

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


# ──────────────────────────────────────────────────────────────
# MCP client  (stdio / JSON-RPC 2.0)
# ──────────────────────────────────────────────────────────────

class Mcp:
    def __init__(self, proc: subprocess.Popen):
        self._proc = proc
        self._id   = 1

    def _send(self, obj: dict) -> None:
        self._proc.stdin.write((json.dumps(obj) + "\n").encode())
        self._proc.stdin.flush()

    def _recv(self) -> dict:
        return json.loads(self._proc.stdout.readline())

    def notify(self, method: str, params: dict | None = None) -> None:
        """Send a JSON-RPC notification — no id, no response expected."""
        msg = {"jsonrpc": "2.0", "method": method}
        if params:
            msg["params"] = params
        self._send(msg)

    def request(self, method: str, params: dict | None = None) -> dict:
        msg = {"jsonrpc": "2.0", "id": self._id, "method": method}
        if params:
            msg["params"] = params
        self._id += 1
        self._send(msg)
        resp = self._recv()
        if "error" in resp:
            raise RuntimeError(resp["error"].get("message", str(resp["error"])))
        return resp.get("result", {})

    def execute(self, command: str, params: dict | None = None) -> dict:
        return self.request(
            "tools/call",
            {"name": "execute", "arguments": {"command": command, "params": params or {}}}
        )

    def close(self):
        try:
            self._proc.stdin.close()
            self._proc.wait(timeout=5)
        except Exception:
            self._proc.kill()


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def find_cli() -> str:
    if shutil.which("solidcraft-cli"):
        return "solidcraft-cli"
    # Windows default install location
    candidate = Path.home() / "AppData" / "Local" / "SolidCraft" / "solidcraft-cli.exe"
    if candidate.exists():
        return str(candidate)
    raise FileNotFoundError(
        "solidcraft-cli not found.\n"
        "Make sure SolidCraft is installed and solidcraft-cli is on PATH."
    )


def launch_mcp(cli: str) -> Mcp:
    proc = subprocess.Popen(
        [cli, "mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    mcp = Mcp(proc)
    mcp.request("initialize", {
        "protocolVersion": "2024-11-05",
        "clientInfo": {"name": "psu-enclosure-designer", "version": "1.0"},
        "capabilities": {}
    })
    mcp.notify("notifications/initialized")
    return mcp


def count_commands(steps: list) -> int:
    return sum(1 for s in steps if "command" in s)


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build PSU enclosure in SolidCraft")
    parser.add_argument("--steps",   default="power_module_steps.json")
    parser.add_argument("--log",     default=None, help="Write timestamped step log here")
    parser.add_argument("--dry-run", action="store_true", help="Validate JSON without connecting")
    args = parser.parse_args()

    path = Path(args.steps)
    if not path.exists():
        sys.exit(f"Steps file not found: {path}")

    with path.open(encoding="utf-8") as f:
        design = json.load(f)

    steps = design.get("steps", [])
    n_cmd = count_commands(steps)
    print(f"Design : {design.get('description', path.name)}")
    print(f"Steps  : {len(steps)}  ({n_cmd} commands)")

    if args.dry_run:
        print("\nDry-run — JSON is valid. No SolidCraft connection made.")
        return

    print("\nOpen SolidCraft and create a NEW empty document, then press Enter …")
    input()

    cli = find_cli()
    print(f"Connecting via {cli} mcp …")
    mcp = launch_mcp(cli)
    print("Connected.\n")

    log_lines: list[str] = []
    t0 = time.monotonic()
    done = 0

    for i, step in enumerate(steps, 1):
        if "comment" in step and "command" not in step:
            print(f"\n  {step['comment']}")
            continue

        command = step.get("command", "")
        params  = step.get("params",  {})
        caption = step.get("caption", command)
        pause   = step.get("pause",   0.3)
        done   += 1

        pct = done * 100 // n_cmd
        print(f"[{pct:3d}%] {caption}")

        try:
            mcp.execute(command, params)
        except RuntimeError as e:
            print(f"       WARNING: {e}")

        elapsed = time.monotonic() - t0
        if args.log:
            log_lines.append(f"{elapsed:8.2f}s  {caption}")

        if pause > 0:
            time.sleep(pause)

    mcp.close()
    print("\nDesign complete.")
    print(f"Save the file in SolidCraft as:  36V_PSU_Enclosure.sc")

    if args.log and log_lines:
        Path(args.log).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        print(f"Log → {args.log}")


if __name__ == "__main__":
    main()
