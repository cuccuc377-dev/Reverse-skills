# mitmproxy AI CLI Usage Rules

This document defines how an AI agent should use the `mitmproxy-ai-cli` capture tool in this project. All paths are relative to the project root.

Current portable runtime entry point:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe
```

Other bundled entry points:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmproxy.exe
tool\mitmproxy-ai-cli-windows-x86_64\mitmdump.exe
tool\mitmproxy-ai-cli-windows-x86_64\mitmweb.exe
tool\mitmproxy-ai-cli-windows-x86_64\_internal
tool\mitmproxy-ai-cli-windows-x86_64\AI_CLI.md
```

Daily use MUST use the compiled runtime under `tool\mitmproxy-ai-cli-windows-x86_64`. Do not run from the source tree for normal capture work.

## 0. Core Purpose

`mitmproxy-ai-cli` is a GUI-free mitmproxy build designed for AI automation. The AI MUST treat it as a scriptable, reproducible, exportable, auditable traffic workbench.

The tool is responsible for:

- Starting a local proxy.
- Capturing HTTP, HTTPS, WebSocket, TCP, UDP, and DNS flows.
- Emitting AI-friendly JSONL.
- Saving native `.mitm` dump files.
- Inspecting `.mitm` or HAR files offline.
- Managing flows through a daemon control API.
- Running mitmproxy internal commands.
- Reading and changing runtime options.

The AI is responsible for:

- Verifying the portable runtime first.
- Creating an isolated task directory.
- Starting `capture` or `daemon`.
- Routing the target client through the proxy.
- Analyzing JSONL, `.mitm`, or HAR evidence.
- Stopping processes and cleaning temporary data when done.

## 1. File Structure Rules

The AI MUST understand this runtime layout:

```text
tool\mitmproxy-ai-cli-windows-x86_64
├── mitmai.exe       # Main AI entry point
├── mitmdump.exe     # Native mitmproxy headless CLI
├── mitmproxy.exe    # In this build, maps to the headless capture entry
├── mitmweb.exe      # GUI disabled; returns a JSON explanation
├── _internal        # Required runtime dependencies
├── AI_CLI.md        # Short usage notes
├── README.md
└── LICENSE
```

`_internal` is required at runtime. MUST NOT copy only one `.exe` to another location. When moving the tool to another computer, copy the whole `tool\mitmproxy-ai-cli-windows-x86_64` folder or extract the full package.

Recommended task directory:

```powershell
work\mitmproxy
```

Recommended per-task layout:

```text
work\mitmproxy\<task_id>
├── flows.jsonl       # Primary AI-readable live capture
├── flows.mitm        # Native mitmproxy dump
├── exports           # Offline exports
├── bodies            # Exported request/response bodies
├── logs              # daemon stdout/stderr
└── notes.md          # Evidence index and conclusions
```

## 2. Entry and Self-Check Rules

ALWAYS verify the main entry first:

```powershell
Test-Path tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe
```

Show main help:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe --help
```

Show version:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmdump.exe --version
```

Confirm GUI-disabled behavior:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmweb.exe
```

Expected behavior: `mitmweb.exe` prints JSON explaining that GUI entry points are disabled. The AI MUST NOT depend on Web GUI or TUI workflows.

## 3. Command Entry Rules

Main command:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe
```

Subcommand responsibilities:

| Command | Purpose |
|---|---|
| `capture` | Start a headless proxy and emit live JSONL |
| `daemon` | Start a proxy plus local control API |
| `inspect` | Read `.mitm` or HAR files and export JSON, JSONL, or summary |
| `flows` | Manage flows in a live daemon |
| `commands` | List or run mitmproxy internal commands |
| `options` | Read, modify, or save runtime options |
| `events` | Read event log entries |
| `state` | Read proxy/backend state |
| `api` | Call any local control API path |
| `gui-disabled` | Explain why GUI entry points are disabled |

Selection rules:

- Use `capture` for one-pass collection.
- Use `daemon` when the AI needs to list, filter, edit, replay, import, or export flows while the proxy is running.
- Use `inspect` for existing `.mitm` or HAR files.
- Use `mitmdump.exe` only when native mitmproxy CLI behavior is specifically needed.
- Do not use `mitmweb.exe` as a work entry point.

## 4. Standard Workflow

### 4.1 Create a Task Directory

```powershell
New-Item -ItemType Directory -Force work\mitmproxy\case001\exports
New-Item -ItemType Directory -Force work\mitmproxy\case001\bodies
New-Item -ItemType Directory -Force work\mitmproxy\case001\logs
```

Recommended evidence files:

```text
work\mitmproxy\case001\flows.jsonl
work\mitmproxy\case001\flows.mitm
work\mitmproxy\case001\notes.md
```

### 4.2 Choose Ports

Default recommendation:

```text
Proxy port:   127.0.0.1:8080
Control port: 127.0.0.1:8081
```

Check port usage before starting:

```powershell
Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 8081 -ErrorAction SilentlyContinue
```

If a port is occupied, the AI SHOULD select another pair such as `18080` and `18081`.

### 4.3 Configure the Target Client Proxy

The target client must route HTTP and HTTPS through:

```text
127.0.0.1:8080
```

The client may be a browser, emulator, app, script, or another tool. The AI MUST record in `notes.md`:

- Proxy address.
- Target client name.
- Target URL or trigger action.
- Whether the mitmproxy CA certificate was installed and trusted.

### 4.4 HTTPS Certificate

HTTPS decryption requires the target client to trust the mitmproxy CA.

Common flow:

```text
1. Start capture or daemon.
2. Set the client proxy to 127.0.0.1:8080.
3. Visit http://mitm.it from the proxied client.
4. Install the certificate for the client platform.
5. Revisit the target and verify HTTPS plaintext visibility.
```

Without the certificate, the AI may still see CONNECT metadata, but not decrypted HTTPS request and response bodies.

## 5. Live Capture Mode

Use `capture` for one-pass collection where live flow editing is not needed.

Recommended command:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture `
  --listen-host 127.0.0.1 `
  --listen-port 8080 `
  --jsonl work\mitmproxy\case001\flows.jsonl `
  --flow-file work\mitmproxy\case001\flows.mitm `
  --body-limit 4096
```

Timed capture:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture `
  --listen-port 8080 `
  --jsonl work\mitmproxy\case001\flows.jsonl `
  --flow-file work\mitmproxy\case001\flows.mitm `
  --duration 60
```

Stream JSONL to stdout:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture --listen-port 8080 --jsonl -
```

Common options:

| Option | Purpose |
|---|---|
| `--listen-host` | Proxy bind address |
| `--listen-port` | Proxy port |
| `--mode` | mitmproxy mode; may be repeated |
| `--jsonl` | JSONL output path; `-` means stdout |
| `--flow-file` | Native `.mitm` dump path |
| `--body-limit` | Request/response body preview byte limit |
| `--headers` / `--no-headers` | Include or omit headers |
| `--bodies` / `--no-bodies` | Include or omit body previews |
| `--duration` | Stop automatically after N seconds |
| `--set option=value` | Pass through mitmproxy options |
| `-s addon.py` | Load an additional mitmproxy addon |

The AI SHOULD save both `flows.jsonl` and `flows.mitm`. JSONL is for fast AI analysis; `.mitm` is for replay, export, and complete review.

## 6. Daemon Control Mode

Use `daemon` for long-running work that needs live flow listing, filtering, editing, replay, import, or export.

Start daemon:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe daemon `
  --listen-host 127.0.0.1 `
  --listen-port 8080 `
  --control-host 127.0.0.1 `
  --control-port 8081 `
  --token mitmai `
  --flow-file work\mitmproxy\case001\flows.mitm `
  --jsonl work\mitmproxy\case001\flows.jsonl `
  --body-limit 4096
```

Recommended background start:

```powershell
$exe = "tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe"
$out = "work\mitmproxy\case001\logs\daemon.out.log"
$err = "work\mitmproxy\case001\logs\daemon.err.log"
$args = @(
  "daemon",
  "--listen-host", "127.0.0.1",
  "--listen-port", "8080",
  "--control-host", "127.0.0.1",
  "--control-port", "8081",
  "--token", "mitmai",
  "--flow-file", "work\mitmproxy\case001\flows.mitm",
  "--jsonl", "work\mitmproxy\case001\flows.jsonl",
  "--body-limit", "4096"
)

$p = Start-Process -FilePath $exe -ArgumentList $args -RedirectStandardOutput $out -RedirectStandardError $err -WindowStyle Hidden -PassThru
```

The control API MUST bind to loopback:

```text
127.0.0.1
```

If a non-loopback control host is required, the AI MUST use a strong token and document the reason in `notes.md`.

## 7. Daemon Control Commands

Shared parameters:

```powershell
--control http://127.0.0.1:8081 --token mitmai
```

Read state:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe state --control http://127.0.0.1:8081 --token mitmai
```

Read events:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe events --control http://127.0.0.1:8081 --token mitmai
```

List flows:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows list --control http://127.0.0.1:8081 --token mitmai
```

Filter flows:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows list --filter "~u /api/" --control http://127.0.0.1:8081 --token mitmai
```

Get one flow:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows get <flow-id> --control http://127.0.0.1:8081 --token mitmai
```

Update flow fields:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows update <flow-id> --json '{"comment":"checked","marked":true}' --control http://127.0.0.1:8081 --token mitmai
```

Replay a flow:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows replay <flow-id> --control http://127.0.0.1:8081 --token mitmai
```

Dump current view:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows dump -o work\mitmproxy\case001\exports\selected.mitm --filter "~u api" --control http://127.0.0.1:8081 --token mitmai
```

Load a dump or HAR:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows load -i work\mitmproxy\case001\flows.mitm --control http://127.0.0.1:8081 --token mitmai
```

Download request or response content:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows content-get <flow-id> response -o work\mitmproxy\case001\bodies\response.bin --control http://127.0.0.1:8081 --token mitmai
```

Render content view:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows content-view <flow-id> response --control http://127.0.0.1:8081 --token mitmai
```

The AI SHOULD use `flows list` to build the map first, then use `flows get` and `content-get` only for selected key flows.

## 8. Commands and Options

List internal mitmproxy commands:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe commands list --control http://127.0.0.1:8081 --token mitmai
```

Run a command:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe commands run replay.client.stop --control http://127.0.0.1:8081 --token mitmai
```

Read all options:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe options get --control http://127.0.0.1:8081 --token mitmai
```

Read one option:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe options get listen_port --control http://127.0.0.1:8081 --token mitmai
```

Set an option:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe options set ssl_insecure true --control http://127.0.0.1:8081 --token mitmai
```

Before changing options, the AI MUST read the current value. After changing options, read the value again to verify.

## 9. Direct API Calls

Use `api` only when `flows`, `commands`, or `options` do not cover the needed operation.

GET:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe api GET /flows.json --control http://127.0.0.1:8081 --token mitmai
```

POST JSON:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe api POST /options --json '{"ssl_insecure":true}' --control http://127.0.0.1:8081 --token mitmai
```

Write response to a file:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe api GET /flows.json -o work\mitmproxy\case001\exports\flows.raw.json --control http://127.0.0.1:8081 --token mitmai
```

## 10. Offline Inspection

Export `.mitm` to JSONL:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe inspect `
  -i work\mitmproxy\case001\flows.mitm `
  --format jsonl `
  -o work\mitmproxy\case001\exports\flows.export.jsonl
```

Generate summary:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe inspect `
  -i work\mitmproxy\case001\flows.mitm `
  --format summary
```

Limit output:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe inspect -i work\mitmproxy\case001\flows.mitm --format json --limit 20
```

Filter while exporting:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe inspect `
  -i work\mitmproxy\case001\flows.mitm `
  --format jsonl `
  --filter "~u /api/" `
  -o work\mitmproxy\case001\exports\api.jsonl
```

Offline analysis order:

```text
summary -> jsonl -> limited json -> selected full body/content
```

Do not dump a large capture file into the terminal as one huge JSON result.

## 11. JSONL Data Rules

Each line is one flow. The AI MUST parse JSONL line by line, not as one JSON array.

Stable fields:

```text
id
type
timestamp_start
client
server
request
response
websocket
tcp
udp
dns
error
```

Body preview fields:

```text
size
sha256
truncated
encoding
preview
```

Rules:

- `preview` is a bounded preview, not the complete body.
- If `truncated=true`, use `.mitm` or `flows content-get` for complete content.
- `sha256` can identify equal bodies.
- Large bodies, binaries, images, and archives should be saved in `bodies`, not pasted into reports.
- Initial parsing SHOULD extract host, path, method, status, content type, size, and body hash.

## 12. Filtering and Analysis Rules

Focus on:

- Non-static resources.
- XHR and fetch APIs.
- JSON, protobuf, form, and multipart requests.
- Non-2xx and non-3xx responses.
- Requests containing token, sign, timestamp, nonce, session, or auth fields.
- Responses containing business data.

Common filter examples:

```text
~u /api/
~m POST
~c 200
~d example.com
~t json
```

Build a request map first:

```text
domain -> path -> method -> status -> content-type -> count
```

Then drill into key requests:

```text
headers -> query -> body -> response -> set-cookie -> replay result
```

## 13. Camoufox and AI IDE Integration

Camoufox opens pages and triggers real browser behavior:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --profile work\camoufox\case001\profile https://example.com
```

mitmproxy AI CLI captures proxy traffic:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture --listen-port 8080 --jsonl work\mitmproxy\case001\flows.jsonl --flow-file work\mitmproxy\case001\flows.mitm
```

Integration rules:

- Browser proxy points to `127.0.0.1:8080`.
- Capture data goes to `work\mitmproxy\<task_id>`.
- Browser screenshots and page state go to `work\camoufox\<task_id>`.
- The two `notes.md` files should reference the same target URL and key timestamps.

If the AI IDE has `camofox-mcp`, use MCP to create tabs and trigger actions, then use `mitmai` for capture.

## 14. Process and Cleanup Rules

Check mitmproxy-related processes:

```powershell
Get-Process | Where-Object { $_.ProcessName -match 'mitm' }
```

Stop the current daemon if `$p` was saved:

```powershell
Stop-Process -Id $p.Id -Force
```

If `$p` was not saved, identify by runtime path before stopping:

```powershell
Get-Process | Where-Object { $_.Path -like "*mitmproxy-ai-cli-windows-x86_64*" } | Select-Object Id,ProcessName,Path
```

MUST NOT kill every process containing `mitm` unless ownership is confirmed.

Before deleting task data, confirm the target is inside `work\mitmproxy`:

```powershell
Remove-Item work\mitmproxy\case001 -Recurse -Force
```

MUST NOT delete:

```text
tool\mitmproxy-ai-cli-windows-x86_64
tool\mitmproxy-ai-cli-windows-x86_64\_internal
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe
```

## 15. Quality Control Rules

Before ending a capture task, the AI MUST verify:

```text
[ ] mitmai.exe path and version recorded
[ ] proxy port and control port recorded
[ ] target client proxy configuration recorded
[ ] HTTPS certificate state recorded
[ ] flows.jsonl saved
[ ] flows.mitm saved
[ ] summary or JSONL export created for key traffic
[ ] truncated bodies completed with content-get or offline export when needed
[ ] key flow IDs recorded
[ ] current daemon or capture process stopped
[ ] temporary logs cleaned or retention reason documented
```

Quality levels:

| Level | Standard |
|---|---|
| A | Commands, ports, flow IDs, JSONL, `.mitm`, key bodies, and reproduction steps |
| B | Commands, JSONL, `.mitm`, and key request list |
| C | Only terminal summary or copied snippets |
| D | No saved capture files; memory-only description |

The AI MUST aim for A or B. C or D may only be temporary observations.

## 16. Quick Command Reference

Help:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe --help
```

Version:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmdump.exe --version
```

Live capture:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture --listen-port 8080 --jsonl work\mitmproxy\case001\flows.jsonl --flow-file work\mitmproxy\case001\flows.mitm
```

Daemon:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe daemon --listen-port 8080 --control-port 8081 --token mitmai --flow-file work\mitmproxy\case001\flows.mitm --jsonl work\mitmproxy\case001\flows.jsonl
```

State:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe state --control http://127.0.0.1:8081 --token mitmai
```

List flows:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe flows list --control http://127.0.0.1:8081 --token mitmai
```

Offline summary:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe inspect -i work\mitmproxy\case001\flows.mitm --format summary
```

Offline JSONL export:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe inspect -i work\mitmproxy\case001\flows.mitm --format jsonl -o work\mitmproxy\case001\exports\flows.export.jsonl
```

## 17. Minimal AI Workflow Template

```text
Task: <target app / target URL / capture purpose>
Working directory: work\mitmproxy\<task_id>

1. Self-check
   - Verify mitmai.exe exists.
   - Run mitmdump.exe --version.
   - Check ports 8080 and 8081.

2. Start
   - Choose capture or daemon.
   - Save flows.jsonl.
   - Save flows.mitm.
   - Record proxy address.

3. Trigger
   - Configure the target client proxy.
   - Visit the target or perform the target action.
   - Install and trust CA if HTTPS plaintext is required.

4. Analyze
   - Start with summary or flows list.
   - Filter API requests.
   - Inspect key flows.
   - Export full bodies.
   - Replay flows if needed.

5. Finish
   - Record key flow IDs.
   - Record evidence file paths.
   - Record verified conclusions.
   - Stop processes.
   - Clean temporary data.
```

## 18. AI Behavior Baseline

- MUST use relative paths for project files.
- MUST use the compiled runtime by default, not the source tree.
- MUST keep `flows.jsonl` and `.mitm` as evidence.
- MUST record proxy port, control port, target client, and trigger action.
- MUST prefer JSONL, JSON, and summary outputs.
- MUST use a token for daemon control API.
- MUST bind the control API to `127.0.0.1`.
- MUST stop current task processes when done.
- MUST NOT delete `tool\mitmproxy-ai-cli-windows-x86_64`.
- MUST NOT copy only one `.exe` to another runtime location.
- MUST NOT treat truncated body preview as a full response.
- MUST NOT replace CLI automation with GUI or TUI operation.
