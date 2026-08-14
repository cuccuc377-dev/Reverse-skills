---
name: reverse-engineering-ai-workbench
description: >
  Use this skill when an AI agent needs to operate this project's reverse-engineering and traffic-analysis toolchain:
  Ghidra AI CLI for static binary analysis, mitmproxy AI CLI for proxy capture and flow control, Camoufox/CamoFox MCP
  for browser automation and dynamic web analysis, or coordinated workflows across these tools. Trigger for tasks
  involving binary import, decompilation, disassembly, strings/imports/xrefs, packet capture, JSONL flow analysis,
  daemon flow replay/editing, browser profile isolation, MCP setup, web interaction, request evidence collection,
  and end-to-end reverse-analysis reports.
---

# Reverse Engineering AI Workbench Skill

## Mandatory Bootstrap Protocol

The first response for any task using this project MUST perform these actions before making changes or drawing conclusions:

1. **Identify the task lane**: classify the request as one or more of `static-binary`, `traffic-capture`, `browser-automation`, `web-dynamic-analysis`, `tool-maintenance`, or `documentation`.
2. **Check the required tool entry**: verify the relevant runtime path exists before use.
3. **Create or choose a task workspace**: use `work\<tool>\<task_id>` for temporary evidence and outputs.
4. **State the initial evidence plan**: list the commands or files that will establish the first reliable facts.
5. **Avoid premature conclusions**: keep hypotheses separate from verified facts until tool output supports them.

Multi-session support: generate a short semantic `task_id` such as `fpscontroller-static-001`, `api-capture-001`, or `camoufox-login-001`. Use that ID consistently for project directories, logs, exports, screenshots, and notes.

## Directory Structure

This project skill uses these core components:

- `SKILL.md`: project-level skill definition and mandatory workflow.
- `guides\Ghidra_AI_CLI_Usage_Rules.md`: detailed rules for Ghidra AI CLI static binary analysis.
- `guides\mitmproxy_AI_CLI_Usage_Rules.md`: detailed rules for mitmproxy AI CLI capture, daemon control, JSONL, and `.mitm` workflows.
- `guides\Camoufox_AI_Usage_Rules.md`: detailed rules for Camoufox, CamoFox MCP, browser profiles, and browser-driven analysis.
- `tool\ghidra_12.2_DEV`: compiled Ghidra AI CLI runtime.
- `tool\ghidra-master`: source or maintenance tree if present; never use it as the default runtime entry.
- `tool\mitmproxy-ai-cli-windows-x86_64`: compiled mitmproxy AI CLI runtime.
- `tool\camoufox_browser`: Camoufox browser runtime and bundled `camofox-mcp` source.
- `work\`: recommended location for generated projects, captures, exports, logs, screenshots, and notes.

Read the relevant detailed rules file before operating that tool. Do not load all references by default if the task only involves one lane.

## Core Philosophy

Use evidence-first reverse engineering. Every conclusion should be backed by a command, path, flow ID, address, request, screenshot, exported file, or reproducible state.

Goal: prevent guesswork, GUI-only workflows, untracked state, and non-reproducible analysis. The AI should behave like a disciplined analyst: map first, inspect selectively, preserve evidence, verify claims, and clean up.

## Input From User or Environment

Collect only what the task requires:

- Target file path, URL, application, or capture objective.
- Desired output: report, patch, capture, replay, static analysis, tool setup, or documentation.
- Runtime constraints: headless/headed browser, ports, profile reuse, timeout, or offline-only analysis.
- Existing artifacts: `.exe`, `.dll`, `.mitm`, HAR, JSONL, screenshots, logs, profiles, or previous notes.
- Required tool lane: Ghidra, mitmproxy, Camoufox, CamoFox MCP, or a coordinated workflow.

If essential input is missing but discoverable locally, inspect the workspace instead of asking immediately.

## Output Contract

The assistant MUST produce task-appropriate outputs:

1. **Evidence summary**: commands run, key files touched, and facts established.
2. **Artifact paths**: generated projects, JSONL files, `.mitm` files, screenshots, exports, logs, or reports.
3. **Verified conclusions**: clearly separate confirmed facts from hypotheses.
4. **Cleanup statement**: note which temporary processes or directories were stopped, removed, or intentionally retained.
5. **Next step**: include only if it directly follows from the evidence.

For analysis tasks, include IDs or anchors such as flow IDs, addresses, function names, URLs, hashes, or screenshot paths.

## Tool Selection Protocol

Select the narrowest tool that can answer the task.

| Task need | Primary tool |
|---|---|
| Binary summary, imports, strings, functions, xrefs, decompile | Ghidra AI CLI |
| Live HTTP/HTTPS proxy capture | mitmproxy AI CLI `capture` |
| Live flow listing, editing, replay, import/export | mitmproxy AI CLI `daemon` |
| Offline `.mitm` or HAR review | mitmproxy AI CLI `inspect` |
| Browser interaction, page snapshots, form workflows, downloads | CamoFox MCP |
| Browser runtime, isolated profile, headed/headless visual checks | Camoufox |
| JS hooks, initiator stacks, JSVMP instrumentation, environment tracing | Camoufox Reverse MCP, when available |
| Browser-triggered API capture | Camoufox or CamoFox MCP plus mitmproxy AI CLI |

## Key Constraints

### Evidence Gate

Never present an unsupported claim as a conclusion.

- Static claims need addresses, strings, imports, functions, xrefs, or decompiler output.
- Traffic claims need flow IDs, URLs, methods, status codes, headers, body hashes, JSONL records, or `.mitm` evidence.
- Browser claims need URL, screenshot, snapshot, DOM output, state export, or tool response.
- Tool setup claims need command output or config path evidence.

### Runtime Gate

Always verify the runtime entry before use:

All relative paths are resolved from the project root, the directory that contains `SKILL.md`, `guides\`, and `tool\`. If the shell starts elsewhere, change to the project root before running these checks.

```powershell
Test-Path tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py
Test-Path tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe
Test-Path tool\camoufox_browser\camoufox\Cache\camoufox.exe
```

For CamoFox MCP, verify build output before writing client config:

```powershell
Test-Path tool\camoufox_browser\camofox-mcp\dist\index.js
```

### Workspace Gate

Use task-local output directories:

```text
work\ghidra_projects
work\mitmproxy\<task_id>
work\camoufox\<task_id>
```

Before recursive deletion, verify the resolved path is under the intended `work` subtree. Never delete `tool\...` runtime directories during cleanup.

### No GUI Dependency

Prefer CLI, MCP, JSON, JSONL, and reproducible scripts. Do not depend on GUI/TUI-only manual actions when a command or MCP tool can do the work.

### State Isolation

Use isolated browser profiles and task-specific capture directories. Do not pollute baseline profiles, shared runtime directories, or unrelated user files.

### Process Ownership

Do not kill broad process classes blindly. Identify process path, port, or saved process ID before stopping a process.

## Static Binary Workflow

Read `guides\Ghidra_AI_CLI_Usage_Rules.md` before using Ghidra.

1. Verify `tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py`.
2. Run a light `one-shot --cmd summary --no-analysis`.
3. For multi-step work, import into `work\ghidra_projects`.
4. Build the map: `functions`, `strings`, `imports`, and summary.
5. Use xrefs, callers, and callees before decompiling deeply.
6. Decompile only selected functions.
7. Save project edits only when the task requires them.
8. Report addresses, function names, strings, and command evidence.

Important: never run parallel commands against the same Ghidra project.

## Traffic Capture Workflow

Read `guides\mitmproxy_AI_CLI_Usage_Rules.md` before using mitmproxy AI CLI.

1. Verify `tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe`.
2. Create `work\mitmproxy\<task_id>\exports`, `bodies`, and `logs`.
3. Check proxy and control ports.
4. Use `capture` for one-pass collection or `daemon` for live flow control.
5. Save both `flows.jsonl` and `flows.mitm`.
6. Configure the target client proxy.
7. Install/trust the mitmproxy CA when HTTPS plaintext is required.
8. Analyze summary and JSONL before exporting full bodies.
9. Stop task-owned capture or daemon processes.

Never treat truncated body previews as full responses. Use `.mitm` or `flows content-get` for complete content.

## Browser and MCP Workflow

Read `guides\Camoufox_AI_Usage_Rules.md` before using Camoufox or CamoFox MCP.

1. Verify `tool\camoufox_browser\camoufox\Cache\camoufox.exe`.
2. Check whether CamoFox MCP tools are already available.
3. If unavailable, build `tool\camoufox_browser\camofox-mcp` and add it to the active AI IDE MCP config.
4. Verify or start `camofox-browser` at `http://localhost:9377`.
5. Use isolated profiles in `work\camoufox\<task_id>\profile`.
6. Prefer `camofox-mcp` for normal navigation, snapshots, clicks, typing, downloads, and profiles.
7. Use Reverse MCP only for hooks, initiator stacks, JSVMP instrumentation, or environment tracing.
8. Save screenshots, page state, relevant requests, and notes.
9. Close tabs or browser sessions and clean task state.

## Coordinated Web Reverse Workflow

For browser-triggered API analysis:

1. Start mitmproxy AI CLI capture or daemon.
2. Configure Camoufox or CamoFox MCP browser traffic through the proxy.
3. Trigger the target page behavior.
4. Preserve browser evidence in `work\camoufox\<task_id>`.
5. Preserve traffic evidence in `work\mitmproxy\<task_id>`.
6. Use JSONL for fast filtering and `.mitm` for complete review.
7. If signing or runtime logic matters, use Reverse MCP for initiator stack, script search, hooks, or environment capture.

## Documentation Workflow

For documentation tasks:

1. Read the relevant existing usage rules first.
2. Keep project paths relative.
3. Write in English unless the user explicitly requests another language.
4. Preserve command correctness; verify command help when practical.
5. Avoid embedding machine-specific absolute paths.
6. Keep the document actionable for another AI agent.

## Quick Start

Ghidra summary:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py one-shot `
  --binary FPSController.exe `
  --cmd summary `
  --no-analysis
```

mitmproxy live capture:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture `
  --listen-port 8080 `
  --jsonl work\mitmproxy\case001\flows.jsonl `
  --flow-file work\mitmproxy\case001\flows.mitm
```

Camoufox direct launch:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --profile work\camoufox\case001\profile https://example.com
```

CamoFox MCP build:

```powershell
Push-Location tool\camoufox_browser\camofox-mcp
npm install
npm run build
Pop-Location
```

## Final Response Checklist

Before the final answer, verify:

- The newest user request is answered.
- The relevant detailed usage rules were followed.
- Generated files are listed with paths.
- Tool output or evidence supports the conclusion.
- Temporary processes and test data are cleaned or intentionally retained.
- Runtime directories under `tool\` were not damaged.
