# Reverse Engineering AI Workbench

An evidence-first Codex skill and bundled Windows toolchain for static binary analysis, HTTP(S) traffic inspection, and browser-driven dynamic analysis.

This project's original material is open source under the [MIT License](LICENSE). Bundled third-party runtimes and assets retain their own licenses and terms; see [Third-Party Notices](THIRD_PARTY_NOTICES.md).

The project gives an AI agent a reproducible operating model for choosing the right reverse-engineering tool, preserving evidence, separating verified facts from hypotheses, and producing analysis artifacts that another operator can inspect and repeat.

> Use this workbench only on software, systems, and traffic you own or are explicitly authorized to test.

## What It Provides

| Analysis lane | Primary runtime | Typical tasks |
|---|---|---|
| Static binary analysis | Ghidra AI CLI | Imports, strings, functions, xrefs, disassembly, decompilation, and project-based analysis |
| Traffic capture | mitmproxy AI CLI | Live HTTP(S) capture, flow filtering, JSONL export, replay, editing, and offline `.mitm` review |
| Browser automation | Camoufox and CamoFox MCP | Isolated browser sessions, navigation, interaction, screenshots, downloads, and profile workflows |
| Web dynamic analysis | Camoufox plus mitmproxy | Browser-triggered API discovery, request evidence, and coordinated runtime analysis |

The repository includes both the instructions an AI agent should follow and the Windows runtimes those instructions reference. Large runtime files are stored with Git LFS.

## Design Principles

- **Evidence first:** conclusions should point to addresses, function names, flow IDs, URLs, hashes, screenshots, exports, or command output.
- **Map before drilling down:** start with summaries, strings, imports, functions, and traffic overviews before expensive deep analysis.
- **Reproducible operation:** prefer CLI, MCP, JSON, JSONL, saved projects, and task-scoped output directories over untracked GUI state.
- **State isolation:** keep browser profiles, captures, projects, and logs outside the bundled runtime directories.
- **Narrow tool selection:** use the smallest tool capable of answering the current question.
- **Controlled cleanup:** stop only task-owned processes and delete only verified paths under the intended `work/` subtree.

## Repository Layout

```text
Reverse-skills/
|-- SKILL.md
|-- guides/
|   |-- Ghidra_AI_CLI_Usage_Rules.md
|   |-- mitmproxy_AI_CLI_Usage_Rules.md
|   |-- Camoufox_AI_Usage_Rules.md
|   `-- thinking/
|       `-- General_Reverse_Engineering_Thinking_Flow.md
|-- tool/
|   |-- ghidra_12.2_DEV/
|   |-- mitmproxy-ai-cli-windows-x86_64/
|   `-- camoufox_browser/
`-- work/                         # Generated locally and ignored by Git
```

Key files:

- [`SKILL.md`](SKILL.md) defines the mandatory bootstrap protocol, tool-selection rules, workflows, and output contract.
- [`guides/Ghidra_AI_CLI_Usage_Rules.md`](guides/Ghidra_AI_CLI_Usage_Rules.md) covers static analysis with Ghidra AI CLI.
- [`guides/mitmproxy_AI_CLI_Usage_Rules.md`](guides/mitmproxy_AI_CLI_Usage_Rules.md) covers capture, daemon control, JSONL, replay, and offline inspection.
- [`guides/Camoufox_AI_Usage_Rules.md`](guides/Camoufox_AI_Usage_Rules.md) covers Camoufox, CamoFox MCP, isolated profiles, and browser evidence.
- [`guides/thinking/General_Reverse_Engineering_Thinking_Flow.md`](guides/thinking/General_Reverse_Engineering_Thinking_Flow.md) provides the general reasoning methodology.

## Requirements

- Windows x86-64.
- Git and [Git LFS](https://git-lfs.com/).
- PowerShell for the documented commands.
- Python and a compatible Java runtime when required by the bundled Ghidra tooling.
- Node.js and npm when rebuilding or modifying CamoFox MCP.
- Administrator privileges only for operations that genuinely require them, such as installing a local interception certificate.

## Installation

Clone with Git LFS enabled. Without LFS, large runtime files will be pointer files and the tools will not run.

```powershell
git lfs install
git clone https://github.com/cuccuc377-dev/Reverse-skills.git
Set-Location Reverse-skills
git lfs pull
```

Verify the runtime entry points before starting work:

```powershell
Test-Path tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py
Test-Path tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe
Test-Path tool\camoufox_browser\camoufox\Cache\camoufox.exe
Test-Path tool\camoufox_browser\camofox-mcp\dist\index.js
```

The first three checks should resolve to `True` for the bundled runtimes. If the CamoFox MCP build output is absent, build it locally:

```powershell
Push-Location tool\camoufox_browser\camofox-mcp
npm install
npm run build
Pop-Location
```

## Using It As A Codex Skill

Install or link this repository as a Codex skill, or open the repository as a Codex project. The agent should read `SKILL.md` first and then load only the guide relevant to the current analysis lane.

Every task starts with the bootstrap protocol:

1. Classify the lane: `static-binary`, `traffic-capture`, `browser-automation`, `web-dynamic-analysis`, `tool-maintenance`, or `documentation`.
2. Verify the required runtime entry point.
3. Choose a short task ID and create a task-local workspace under `work/`.
4. State which commands and artifacts will establish the initial facts.
5. Keep hypotheses separate from verified conclusions.

## Quick Start

### Static Binary Summary

Read the Ghidra guide before operating the CLI, then run a lightweight summary:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py one-shot `
  --binary C:\path\to\sample.exe `
  --cmd summary `
  --no-analysis
```

For multi-step analysis, create a persistent project under `work\ghidra_projects`, map functions/strings/imports first, and decompile only selected functions.

### HTTP(S) Traffic Capture

Create a task directory and preserve both a searchable JSONL export and the complete mitmproxy flow file:

```powershell
$taskId = "api-capture-001"
New-Item -ItemType Directory -Force "work\mitmproxy\$taskId\logs" | Out-Null

tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture `
  --listen-port 8080 `
  --jsonl "work\mitmproxy\$taskId\flows.jsonl" `
  --flow-file "work\mitmproxy\$taskId\flows.mitm"
```

Configure only the authorized target client to use the proxy. HTTPS plaintext inspection may require installing and trusting the mitmproxy CA certificate.

### Camoufox Browser Session

Launch Camoufox with an isolated task profile rather than writing state into the bundled runtime:

```powershell
$taskId = "browser-analysis-001"
New-Item -ItemType Directory -Force "work\camoufox\$taskId\profile" | Out-Null

tool\camoufox_browser\camoufox\Cache\camoufox.exe `
  --new-instance `
  --profile "work\camoufox\$taskId\profile" `
  https://example.com
```

Use CamoFox MCP for normal navigation, snapshots, clicks, typing, downloads, and profile operations. Preserve relevant screenshots, page state, URLs, and request evidence in the task directory.

## Coordinated Web Analysis

A browser-triggered API investigation typically follows this sequence:

1. Start mitmproxy capture or daemon mode using task-specific ports and output paths.
2. Route an isolated Camoufox session through that proxy.
3. Trigger the authorized behavior in the browser.
4. Preserve browser screenshots and state under `work\camoufox\<task_id>`.
5. Preserve JSONL and `.mitm` evidence under `work\mitmproxy\<task_id>`.
6. Filter and summarize JSONL first; retrieve full bodies from the `.mitm` file only when needed.
7. Report flow IDs, methods, URLs, status codes, hashes, and artifact paths.

## Output Contract

An analysis result should contain:

- **Evidence summary:** commands run and facts established.
- **Artifact paths:** projects, captures, exports, screenshots, logs, and reports.
- **Verified conclusions:** claims tied to concrete evidence.
- **Hypotheses:** clearly marked assumptions that still require validation.
- **Cleanup statement:** processes stopped and temporary state retained or removed.
- **Next step:** only when it follows directly from the evidence.

## Generated Data And Security

The repository intentionally ignores runtime-generated and potentially sensitive state, including:

- Camoufox browser profiles, cookies, storage, startup cache, and downloads.
- Ghidra Python and Gradle caches.
- `work/` projects, captures, logs, screenshots, and exported bodies.
- `.mitm`, HAR, JSONL, log, environment, and temporary files.

Review `git status` before every commit. Never commit live browser profiles, credentials, private certificates, captured authentication material, proprietary samples, or analysis evidence that you are not authorized to publish.

## Git LFS

Seventeen large runtime files are managed by Git LFS. Useful checks:

```powershell
git lfs install
git lfs pull
git lfs ls-files
git lfs fsck
```

Cloning and downloading the bundled runtimes consumes Git LFS storage and bandwidth from the repository owner's GitHub quota.

## Updating Bundled Tools

When replacing a bundled runtime:

1. Stop processes that are using the runtime.
2. Preserve only distributable runtime files, not local profiles or generated evidence.
3. Verify the documented entry point and version.
4. Check files larger than 100 MB and add them to Git LFS before committing.
5. Run a minimal help or summary command.
6. Update the relevant guide and this README when paths or behavior change.

## License And Third-Party Components

Original project material is released under the OSI-approved [MIT License](LICENSE). The repository also bundles third-party software, binaries, fonts, and supporting data that remain subject to their own licenses and terms.

Read [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and the license files within each runtime directory before redistributing, mirroring, or using bundled assets outside their original tool context. Pay particular attention to fonts and binary distributions, which may carry terms beyond the project's MIT License.

## Disclaimer

Reverse engineering and traffic interception can expose sensitive data and may be restricted by contracts or law. You are responsible for obtaining authorization, limiting collection, protecting captured data, and complying with all applicable requirements.
