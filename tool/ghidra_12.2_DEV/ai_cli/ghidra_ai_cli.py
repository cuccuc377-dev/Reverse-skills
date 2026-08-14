#!/usr/bin/env python3
"""
Command-line bridge for AI-friendly Ghidra headless workflows.

This wrapper invokes Ghidra's analyzeHeadless launcher and runs
AiCommandScript.java. All normal results are printed as JSON.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
GHIDRA_SCRIPT_DIR = SCRIPT_DIR / "scripts"
ENCODED_ARG_PREFIX = "__b64_"


def find_ghidra_root(explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("GHIDRA_HOME"):
        candidates.append(Path(os.environ["GHIDRA_HOME"]))
    candidates.append(SCRIPT_DIR.parent)

    for candidate in candidates:
        root = candidate.resolve()
        if find_analyze_headless(root):
            return root
    raise SystemExit(
        "Could not find Ghidra analyzeHeadless. Pass --ghidra or set GHIDRA_HOME."
    )


def find_analyze_headless(root: Path) -> Path | None:
    names = ["analyzeHeadless.bat", "analyzeHeadless"] if os.name == "nt" else [
        "analyzeHeadless",
        "analyzeHeadless.bat",
    ]
    dirs = [
        root / "support",
        root / "Ghidra" / "RuntimeScripts" / "support",
    ]
    for directory in dirs:
        for name in names:
            path = directory / name
            if path.exists():
                return path
    return None


def base_headless_args(args: argparse.Namespace) -> list[str]:
    root = find_ghidra_root(args.ghidra)
    analyze = find_analyze_headless(root)
    assert analyze is not None
    cmd = [str(analyze), str(Path(args.project_dir).resolve()), args.project_name]
    return cmd


def add_common_headless_options(cmd: list[str], args: argparse.Namespace) -> None:
    if getattr(args, "no_analysis", False):
        cmd.append("-noanalysis")
    timeout = getattr(args, "analysis_timeout", None)
    if timeout:
        cmd.extend(["-analysisTimeoutPerFile", str(timeout)])
    max_cpu = getattr(args, "max_cpu", None)
    if max_cpu:
        cmd.extend(["-max-cpu", str(max_cpu)])
    if getattr(args, "read_only", False):
        cmd.append("-readOnly")
    if getattr(args, "delete_project", False):
        cmd.append("-deleteProject")


def script_args(args: argparse.Namespace, out_file: Path) -> list[str]:
    result = [
        "-scriptPath",
        str(GHIDRA_SCRIPT_DIR),
        "-postScript",
        "AiCommandScript.java",
        script_arg("out", str(out_file)),
        script_arg("cmd", args.cmd),
    ]
    script_keys = [
        "address",
        "entry",
        "end",
        "end_address",
        "body_start",
        "body_end",
        "name",
        "function",
        "filter",
        "limit",
        "offset",
        "timeout",
        "hex",
        "bytes",
        "length",
        "count",
        "min",
        "max",
        "depth",
        "new_name",
        "to",
        "label",
        "comment",
        "comment_type",
        "target",
        "signature",
        "type",
        "datatype",
        "struct_name",
        "fields",
        "category",
        "assembly",
        "asm",
        "var",
        "variable",
        "var_kind",
        "kind",
        "index",
        "size",
        "clear_mode",
        "source",
        "conflict",
        "calling_convention",
        "flag",
        "enabled",
        "option",
        "value",
        "analysis_option",
        "analysis_value",
        "format",
        "output",
        "symbol_id",
        "id",
    ]
    for key in script_keys:
        value = getattr(args, key, None)
        if value is not None:
            result.append(script_arg(key, str(value)))
    for key in [
        "force",
        "rename",
        "primary",
        "clear",
        "align",
        "preserve_calling_convention",
        "clear_context",
        "changes_only",
        "address_only",
    ]:
        value = getattr(args, key, None)
        if value:
            result.append(script_arg(key, "true"))
    for item in getattr(args, "script_arg", []) or []:
        if "=" not in item:
            raise SystemExit(f"--script-arg must use key=value form: {item}")
        key, value = item.split("=", 1)
        result.append(script_arg(key, value))
    return result


def script_arg(key: str, value: str) -> str:
    encoded = base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii").rstrip("=")
    return f"{ENCODED_ARG_PREFIX}{key}={encoded}"


def run_headless(cmd: list[str], out_file: Path, show_log: bool) -> int:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if out_file.exists():
        text = out_file.read_text(encoding="utf-8", errors="replace")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {"ok": False, "error": "Invalid JSON emitted by Ghidra script", "raw": text}
        payload["_headless_returncode"] = proc.returncode
        if show_log:
            payload["_headless_stdout"] = proc.stdout
            payload["_headless_stderr"] = proc.stderr
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return proc.returncode

    payload = {
        "ok": False,
        "error": "Ghidra script did not produce an output JSON file",
        "headless_returncode": proc.returncode,
        "headless_stdout": proc.stdout,
        "headless_stderr": proc.stderr,
        "command": cmd,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return proc.returncode or 1


def build_import_command(args: argparse.Namespace, out_file: Path) -> list[str]:
    cmd = base_headless_args(args)
    cmd.extend(["-import", str(Path(args.binary).resolve())])
    if args.overwrite:
        cmd.append("-overwrite")
    add_common_headless_options(cmd, args)
    cmd.extend(script_args(args, out_file))
    return cmd


def build_process_command(args: argparse.Namespace, out_file: Path) -> list[str]:
    cmd = base_headless_args(args)
    cmd.extend(["-process", args.process])
    add_common_headless_options(cmd, args)
    cmd.extend(script_args(args, out_file))
    return cmd


def add_project_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ghidra", help="Ghidra root directory. Defaults to GHIDRA_HOME or this tree.")
    parser.add_argument("--project-dir", required=True, help="Directory containing or receiving the Ghidra project.")
    parser.add_argument("--project-name", required=True, help="Ghidra project name.")
    parser.add_argument("--analysis-timeout", type=int, help="Headless analysis timeout per file, in seconds.")
    parser.add_argument("--max-cpu", type=int, help="Maximum CPU cores used by Ghidra analysis.")
    parser.add_argument("--show-log", action="store_true", help="Include analyzeHeadless stdout/stderr in JSON.")


def add_command_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--cmd", default="summary", help="AiCommandScript command.")
    parser.add_argument("--address", help="Address for the command.")
    parser.add_argument("--entry", help="Function entry address.")
    parser.add_argument("--end", help="End address for range commands.")
    parser.add_argument("--end-address", dest="end_address", help="End address for range commands.")
    parser.add_argument("--body-start", dest="body_start", help="Function body start address.")
    parser.add_argument("--body-end", dest="body_end", help="Function body end address.")
    parser.add_argument("--name", help="Name used by function/symbol/type commands.")
    parser.add_argument("--function", help="Function name or entry address for variable commands.")
    parser.add_argument("--filter", help="Substring filter for functions/strings/symbols.")
    parser.add_argument("--limit", type=int, help="Maximum number of rows.")
    parser.add_argument("--offset", type=int, help="Pagination offset.")
    parser.add_argument("--timeout", type=int, help="Decompiler timeout, in seconds.")
    parser.add_argument("--hex", help="Hex bytes for search-bytes.")
    parser.add_argument("--bytes", help="Hex bytes for patch-bytes.")
    parser.add_argument("--length", type=int, help="Byte count for read-memory.")
    parser.add_argument("--count", type=int, help="Alias count for read-memory.")
    parser.add_argument("--min", type=int, help="Minimum string length for strings command.")
    parser.add_argument("--max", type=int, help="Maximum value for commands that use one.")
    parser.add_argument("--depth", type=int, help="Graph traversal depth.")
    parser.add_argument("--new-name", dest="new_name", help="New function/symbol/variable name.")
    parser.add_argument("--to", help="Alias for --new-name.")
    parser.add_argument("--label", help="Label name for create-label.")
    parser.add_argument("--comment", help="Comment text.")
    parser.add_argument("--comment-type", dest="comment_type", help="Comment type: eol/pre/post/plate/repeatable.")
    parser.add_argument("--target", help="Target kind, for example function or code.")
    parser.add_argument("--signature", help="Function signature text.")
    parser.add_argument("--type", help="Data type text.")
    parser.add_argument("--datatype", help="Alias for --type.")
    parser.add_argument("--struct-name", dest="struct_name", help="Structure type name.")
    parser.add_argument("--fields", help="Structure fields, e.g. 0:uint32_t:magic;4:char[16]:name.")
    parser.add_argument("--category", help="Data type category path.")
    parser.add_argument("--assembly", help="Assembly text for assemble.")
    parser.add_argument("--asm", help="Alias for --assembly.")
    parser.add_argument("--var", help="Variable name.")
    parser.add_argument("--variable", help="Alias for --var.")
    parser.add_argument("--var-kind", dest="var_kind", help="Variable kind: all/param/local/return.")
    parser.add_argument("--kind", help="Generic kind argument.")
    parser.add_argument("--index", type=int, help="Variable index.")
    parser.add_argument("--size", type=int, help="Size for type/structure commands.")
    parser.add_argument("--clear-mode", dest="clear_mode", help="Data clearing mode for apply-type.")
    parser.add_argument("--source", help="Ghidra SourceType, defaults to USER_DEFINED.")
    parser.add_argument("--conflict", help="Data type conflict policy: replace/keep/rename.")
    parser.add_argument("--calling-convention", dest="calling_convention", help="Calling convention name.")
    parser.add_argument("--flag", help="Function flag: noreturn/inline/varargs/custom_storage.")
    parser.add_argument("--enabled", help="Boolean flag value.")
    parser.add_argument("--option", help="Analysis option name.")
    parser.add_argument("--value", help="Generic value argument.")
    parser.add_argument("--analysis-option", dest="analysis_option", help="Analysis option name.")
    parser.add_argument("--analysis-value", dest="analysis_value", help="Analysis option value.")
    parser.add_argument("--format", help="Output format hint for export commands.")
    parser.add_argument("--output", help="Output path hint for export commands.")
    parser.add_argument("--symbol-id", dest="symbol_id", help="Symbol id.")
    parser.add_argument("--id", help="Generic id.")
    parser.add_argument("--force", action="store_true", help="Force variable/type edits where supported.")
    parser.add_argument("--rename", action="store_true", help="Allow signature command to rename the function.")
    parser.add_argument("--primary", action="store_true", help="Make a created label primary.")
    parser.add_argument("--clear", action="store_true", help="Clear a comment instead of setting text.")
    parser.add_argument("--align", action="store_true", help="Align stack variable type changes.")
    parser.add_argument("--preserve-calling-convention", dest="preserve_calling_convention", action="store_true")
    parser.add_argument("--clear-context", dest="clear_context", action="store_true")
    parser.add_argument("--changes-only", dest="changes_only", action="store_true", help="Analyze only pending changes.")
    parser.add_argument("--address-only", dest="address_only", action="store_true", help="Do not resolve address to containing function.")
    parser.add_argument(
        "--script-arg",
        action="append",
        default=[],
        help="Extra key=value argument passed directly to AiCommandScript.java.",
    )


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI-friendly Ghidra headless command bridge.")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_import = sub.add_parser("import", help="Import a binary, analyze it, and run one command.")
    add_project_args(p_import)
    add_command_args(p_import)
    p_import.add_argument("--binary", required=True, help="Binary to import.")
    p_import.add_argument("--overwrite", action="store_true", help="Overwrite existing imported program.")
    p_import.add_argument("--no-analysis", action="store_true", help="Import without auto-analysis.")
    p_import.add_argument("--read-only", action="store_true", help="Open project read-only.")
    p_import.add_argument("--delete-project", action="store_true", help="Delete project after run.")

    p_process = sub.add_parser("run", help="Run one command against an existing project program.")
    add_project_args(p_process)
    add_command_args(p_process)
    p_process.add_argument("--process", required=True, help="Program name/path inside the Ghidra project.")
    p_process.add_argument("--analyze", action="store_true", help="Run analysis before the command.")
    p_process.add_argument("--read-only", action="store_true", help="Open project read-only.")
    p_process.set_defaults(no_analysis=True, delete_project=False)

    p_one = sub.add_parser("one-shot", help="Create a temp project, import a binary, run one command, delete it.")
    p_one.add_argument("--ghidra", help="Ghidra root directory. Defaults to GHIDRA_HOME or this tree.")
    add_command_args(p_one)
    p_one.add_argument("--binary", required=True, help="Binary to import.")
    p_one.add_argument("--analysis-timeout", type=int, help="Headless analysis timeout per file, in seconds.")
    p_one.add_argument("--max-cpu", type=int, help="Maximum CPU cores used by Ghidra analysis.")
    p_one.add_argument("--show-log", action="store_true", help="Include analyzeHeadless stdout/stderr in JSON.")
    p_one.add_argument("--no-analysis", action="store_true", help="Import without auto-analysis.")
    p_one.set_defaults(project_name="ai_tmp", overwrite=True, delete_project=True, read_only=False)
    return parser


def main(argv: list[str]) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)

    temp_dir_obj = None
    if args.mode == "one-shot":
        temp_dir_obj = tempfile.TemporaryDirectory(prefix="ghidra-ai-")
        args.project_dir = temp_dir_obj.name

    fd, out_name = tempfile.mkstemp(prefix="ghidra-ai-result-", suffix=".json")
    os.close(fd)
    out_file = Path(out_name)
    try:
        if args.mode in ("import", "one-shot"):
            cmd = build_import_command(args, out_file)
        else:
            if args.analyze:
                args.no_analysis = False
            cmd = build_process_command(args, out_file)
        return run_headless(cmd, out_file, args.show_log)
    finally:
        try:
            out_file.unlink(missing_ok=True)
        finally:
            if temp_dir_obj is not None:
                temp_dir_obj.cleanup()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
