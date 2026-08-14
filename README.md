# Reverse Engineering AI Workbench

An evidence-first Codex skill for coordinating static binary analysis, HTTP(S) traffic capture, and browser-driven dynamic analysis.

The repository contains the skill definition and operating guides. Third-party runtimes, browser profiles, captures, logs, and generated analysis artifacts are intentionally excluded from Git because they are large, machine-specific, or potentially sensitive.

## Included

- `SKILL.md`: skill definition and workflow contract.
- `guides/Ghidra_AI_CLI_Usage_Rules.md`: Ghidra AI CLI usage rules.
- `guides/mitmproxy_AI_CLI_Usage_Rules.md`: mitmproxy AI CLI usage rules.
- `guides/Camoufox_AI_Usage_Rules.md`: Camoufox and CamoFox MCP usage rules.
- `guides/thinking/General_Reverse_Engineering_Thinking_Flow.md`: general analysis methodology.

## Local Runtime Layout

Install or place the required third-party runtimes under `tool/`:

```text
tool/
|-- ghidra_12.2_DEV/
|-- mitmproxy-ai-cli-windows-x86_64/
`-- camoufox_browser/
```

Generated evidence belongs under `work/`. See `SKILL.md` and the relevant guide before operating a tool.

## Usage

Install this directory as a Codex skill, or open it as a project and follow the bootstrap protocol in `SKILL.md`. Verify each runtime entry before starting an analysis task.
