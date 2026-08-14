# Camoufox AI Usage Rules

This document defines how an AI agent should use the Camoufox browser runtime in this project. All paths are relative to the project root.

Current browser entry point:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe
```

Browser configuration and policy files:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.cfg
tool\camoufox_browser\camoufox\Cache\properties.json
tool\camoufox_browser\camoufox\Cache\distribution\policies.json
```

Profile directory:

```powershell
tool\camoufox_browser\Profiles
```

Bundled MCP server source:

```powershell
tool\camoufox_browser\camofox-mcp
```

## 0. Core Purpose

Camoufox is the anti-detection browser runtime for AI tasks. The AI MUST treat it as a controllable, reproducible, evidence-preserving, cleanable dynamic analysis environment, not as a normal manual browser.

Camoufox is responsible for:

- Running target pages in a fixed browser runtime.
- Providing realistic browser environment surfaces such as `navigator`, `screen`, canvas, WebGL, Audio, fonts, locale, timezone, and related fingerprint fields.
- Supporting headed and headless operation.
- Supporting isolated profiles for cookies, cache, extensions, and local storage.
- Supporting remote debugging, DevTools, Marionette, MCP, and automation clients.

The AI is responsible for:

- Verifying browser path, version, and process state.
- Choosing an isolated or temporary profile.
- Starting the browser directly or through MCP.
- Preserving evidence: URL, screenshot, request data, scripts, cookies, environment values, and console logs.
- Closing processes and cleaning temporary profiles and artifacts after the task.

## 1. File Structure Rules

The AI MUST understand this directory layout:

```text
tool\camoufox_browser
├── camoufox
│   └── Cache              # Browser binary, config, fonts, extensions, runtime libraries
├── Profiles               # Browser profiles, cache, and local state
└── camofox-mcp            # MCP server project for AI IDE clients
```

`camoufox\Cache` is the browser runtime directory. The AI MUST NOT modify, delete, or rename files there during normal work.

`Profiles` is the browser state directory. The AI may create task-specific profiles, but MUST avoid polluting baseline profiles.

`camofox-mcp` is a generic MCP server project. AI IDEs such as Trae, Codex, Cursor, CodeBuddy, VS Code, and Claude Desktop should use it when they support MCP.

Recommended AI task directory:

```powershell
work\camoufox
```

Recommended per-task layout:

```text
work\camoufox\<task_id>
├── profile          # Isolated profile for this task
├── screenshots      # Screenshots
├── network          # Requests, HAR, JSONL, response samples
├── scripts          # Saved JS, WASM, and HTML fragments
├── env              # Environment collection and diff results
└── notes.md         # Evidence index and conclusions
```

## 2. Browser Entry Rules

### 2.1 Basic Self-Check

ALWAYS verify the browser entry:

```powershell
Test-Path tool\camoufox_browser\camoufox\Cache\camoufox.exe
```

Check version:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --version
```

Read bundled version metadata:

```powershell
Get-Content tool\camoufox_browser\camoufox\Cache\version.json
```

This project currently bundles Firefox/Camoufox `135.0.1-beta.24`.

### 2.2 Direct Browser Launch

Open a page:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance https://example.com
```

Use an isolated profile:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --profile work\camoufox\case001\profile https://example.com
```

Headless screenshot:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --headless --screenshot work\camoufox\case001\screenshots\home.png --window-size 1365,768 https://example.com
```

Start DevTools remote debugging:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --start-debugger-server 6000 --profile work\camoufox\case001\profile https://example.com
```

Start Marionette:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --marionette --profile work\camoufox\case001\profile https://example.com
```

Direct browser launch is a fallback. If MCP is available, prefer MCP.

## 3. MCP Auto-Detection and Installation Rules

The AI MUST prefer MCP for Camoufox control. Direct `camoufox.exe` launch is only a fallback.

Bundled CamoFox MCP source:

```powershell
tool\camoufox_browser\camofox-mcp
```

The MCP project is Node.js / TypeScript and requires Node.js `18+`. Runtime entries are produced by build:

```powershell
tool\camoufox_browser\camofox-mcp\dist\index.js
tool\camoufox_browser\camofox-mcp\dist\http.js
```

Important: `camofox-mcp` is not a standalone browser. It connects to a `camofox-browser` service. Default service URL:

```text
http://localhost:9377
```

### 3.1 Auto-Detection Flow

Before any Camoufox task in an MCP-capable AI IDE or agent, the AI MUST follow this chain:

```text
1. Check whether CamoFox MCP tools are already exposed in the current tool list.
2. If not exposed, scan common AI IDE MCP config files.
3. If no camofox-mcp config exists, build the local MCP project.
4. Add camofox-mcp to the current IDE or agent MCP config.
5. Check whether the camofox-browser service is running.
6. If the browser service is not running, start it automatically or report that IDE restart is required.
7. Verify server_status, create_tab, navigate_and_snapshot, and close_tab.
```

Minimum tool set indicating CamoFox MCP is available:

```text
server_status
create_tab
navigate
navigate_and_snapshot
snapshot
click
type_text
close_tab
```

If the current environment can list MCP tools, ALWAYS check for these tools first. Do not install a duplicate server if it already exists.

### 3.2 Local MCP Build Check

Check Node.js:

```powershell
node --version
npm --version
```

Node.js must be `>=18.0.0`. If Node.js is missing, the AI SHOULD install Node.js LTS. On Windows:

```powershell
winget install OpenJS.NodeJS.LTS
```

Build the local MCP project:

```powershell
Push-Location tool\camoufox_browser\camofox-mcp
npm install
npm run build
Pop-Location
```

Verify build output:

```powershell
Test-Path tool\camoufox_browser\camofox-mcp\dist\index.js
Test-Path tool\camoufox_browser\camofox-mcp\dist\http.js
```

If `dist\index.js` does not exist, MUST NOT write MCP client config. Fix the build first.

### 3.3 Browser Service Check

Check `camofox-browser`:

```powershell
try {
  Invoke-RestMethod http://localhost:9377/health
} catch {
  Write-Output "camofox-browser is not running"
}
```

If the service is missing, start it:

```powershell
Start-Process -FilePath "npx" -ArgumentList @("-y", "camofox-browser@latest") -WindowStyle Hidden
```

Verify again:

```powershell
Invoke-RestMethod http://localhost:9377/health
```

Expected response includes:

```json
{
  "ok": true
}
```

On cold start, `browserConnected` may be `false`. That is not always failure. Create the first tab before judging browser session health.

### 3.4 Multi-IDE Config Scan

The AI MUST NOT detect Codex only. Scan all common client locations and skip missing files:

```powershell
$candidateFiles = @(
  ".cursor\mcp.json",
  ".trae\mcp.json",
  ".codebuddy\mcp.json",
  ".vscode\mcp.json",
  "$env:USERPROFILE\.cursor\mcp.json",
  "$env:USERPROFILE\.trae\mcp.json",
  "$env:USERPROFILE\.codebuddy\mcp.json",
  "$env:USERPROFILE\.codex\config.toml",
  "$env:APPDATA\Cursor\User\mcp.json",
  "$env:APPDATA\Trae\User\mcp.json",
  "$env:APPDATA\Trae CN\User\mcp.json",
  "$env:APPDATA\CodeBuddy\User\mcp.json",
  "$env:APPDATA\CodeBuddy CN\User\mcp.json",
  "$env:APPDATA\Code\User\mcp.json",
  "$env:APPDATA\Claude\claude_desktop_config.json"
)

$candidateFiles | Where-Object { Test-Path $_ } | ForEach-Object {
  Select-String -Path $_ -Pattern @("camofox", "camofox-mcp", "CAMOFOX_URL") -SimpleMatch
}
```

If an existing `camofox` or `camofox-mcp` entry is found:

- MUST NOT add a duplicate entry.
- MUST verify that `command`, `args`, and `env` still point to a usable entry.
- If the entry is broken, update only that entry. Do not rewrite unrelated config.

### 3.5 Generic JSON MCP Config

Cursor, Trae, CodeBuddy, Claude Desktop, and many VS Code-style IDEs commonly use JSON MCP config. The AI MUST preserve the existing schema:

- If the file has top-level `mcpServers`, write `mcpServers.camofox`.
- If the file has top-level `servers`, write `servers.camofox`.
- For new Cursor, Trae, CodeBuddy, or Claude Desktop config, prefer `mcpServers`.
- For new VS Code config, prefer `servers`.

Generic `mcpServers` template:

```json
{
  "mcpServers": {
    "camofox": {
      "command": "node",
      "args": ["<resolved-project-root>\\tool\\camoufox_browser\\camofox-mcp\\dist\\index.js"],
      "env": {
        "CAMOFOX_URL": "http://localhost:9377",
        "CAMOFOX_PROFILES_DIR": "<resolved-project-root>\\work\\camoufox\\mcp-profiles",
        "CAMOFOX_VIEWPORT": "1366x768"
      }
    }
  }
}
```

Generic `servers` template:

```json
{
  "servers": {
    "camofox": {
      "type": "stdio",
      "command": "node",
      "args": ["<resolved-project-root>\\tool\\camoufox_browser\\camofox-mcp\\dist\\index.js"],
      "env": {
        "CAMOFOX_URL": "http://localhost:9377",
        "CAMOFOX_PROFILES_DIR": "<resolved-project-root>\\work\\camoufox\\mcp-profiles",
        "CAMOFOX_VIEWPORT": "1366x768"
      }
    }
  }
}
```

Documentation paths remain relative. When writing an actual IDE config, the AI MUST resolve real paths because the IDE may not start from the project root:

```powershell
$mcpEntry = (Resolve-Path "tool\camoufox_browser\camofox-mcp\dist\index.js").Path
$profiles = (New-Item -ItemType Directory -Force "work\camoufox\mcp-profiles").FullName
```

Backup before editing config:

```powershell
Copy-Item $configPath "$configPath.bak-camofox-mcp" -Force
```

### 3.6 Codex TOML Config

Codex TOML config path:

```powershell
$env:USERPROFILE\.codex\config.toml
```

Template:

```toml
[mcp_servers.camofox]
type = "stdio"
command = "node"
args = ["<resolved-project-root>\\tool\\camoufox_browser\\camofox-mcp\\dist\\index.js"]
startup_timeout_sec = 120

[mcp_servers.camofox.env]
CAMOFOX_URL = "http://localhost:9377"
CAMOFOX_PROFILES_DIR = "<resolved-project-root>\\work\\camoufox\\mcp-profiles"
CAMOFOX_VIEWPORT = "1366x768"
```

If `[mcp_servers.camofox]` already exists, update only that section.

### 3.7 Trae, Cursor, and CodeBuddy Rules

Trae, Cursor, and CodeBuddy config formats may vary by version. Use discovery first:

```text
1. Check project-level directories: .trae, .cursor, .codebuddy, .vscode.
2. Check user-level hidden directories.
3. Check AppData IDE User directories.
4. Read existing JSON top-level fields.
5. Preserve the existing schema and add or update only the camofox entry.
```

Do not assume every IDE uses the same file name. If no config exists, create the most common project-level config and report the path.

Recommended new project-level paths:

```text
.cursor\mcp.json
.trae\mcp.json
.codebuddy\mcp.json
.vscode\mcp.json
```

Project-level config is preferred because it travels with the project.

### 3.8 HTTP Transport Rules

Most desktop AI IDEs should use `stdio`. Use HTTP transport only for remote agents, web IDEs, or OpenClaw-like clients.

Local HTTP start:

```powershell
$env:CAMOFOX_TRANSPORT = "http"
$env:CAMOFOX_HTTP_HOST = "127.0.0.1"
$env:CAMOFOX_HTTP_PORT = "3000"
node tool\camoufox_browser\camofox-mcp\dist\http.js
```

If HTTP binds outside loopback, MUST set a Bearer token of at least 32 characters:

```powershell
$env:CAMOFOX_HTTP_API_KEY = "<32-plus-random-chars>"
```

MUST NOT expose unauthenticated HTTP MCP to LAN or public networks.

### 3.9 Post-Install Verification

After writing config, the IDE usually needs restart. After restart, verify:

```text
server_status
create_tab(url="https://example.com", userId="setup-test", viewport={width:1366,height:768})
navigate_and_snapshot(tabId="<tabId>", url="https://example.com")
close_tab(tabId="<tabId>")
```

Pass criteria:

- `server_status` reaches `http://localhost:9377`.
- `create_tab` returns `tabId`.
- `navigate_and_snapshot` returns page content containing `Example Domain`.
- `close_tab` releases the tab.

### 3.10 CamoFox MCP Tool Map

| Goal | Preferred tool |
|---|---|
| Service health | `server_status` |
| New tab | `create_tab` |
| Open page | `navigate` / `navigate_and_snapshot` |
| Page structure | `snapshot` |
| Visual proof | `screenshot` |
| Click and type | `click` / `type_text` / `type_and_submit` / `fill_form` |
| Wait for loading | `camofox_wait_for` / `camofox_wait_for_selector` / `camofox_wait_for_text` |
| DOM query | `camofox_query_selector` / `camofox_get_page_html` |
| JavaScript | `camofox_evaluate_js` |
| Links | `get_links` |
| Structured extraction | `extract_structured` |
| Downloads | `list_downloads` / `get_download` / `delete_download` |
| Profiles | `save_profile` / `load_profile` / `list_profiles` / `delete_profile` |
| Cleanup | `close_tab` / `camofox_close_session` |

### 3.11 Reverse MCP Compatibility

If Camoufox Reverse MCP is also available and the task requires reverse engineering, hooks, JSVMP instrumentation, request initiator stacks, or environment tracing, prefer Reverse MCP:

```text
check_environment
launch_browser
navigate
network_capture
get_request_initiator
scripts / search_code
evaluate_js / hook_function / inject_hook_preset
instrumentation / trace_property_access
reset_browser_state / close_browser
```

If the task is ordinary browsing, form interaction, page extraction, downloads, or profile reuse, prefer `camofox-mcp`.

MUST NOT replace scriptable operations with manual clicking. Use screenshots only when visual confirmation is needed.

## 4. Profile Management Rules

### 4.1 Default Strategy

ALWAYS create an isolated profile for a new task:

```powershell
New-Item -ItemType Directory -Force work\camoufox\case001\profile
```

Launch with that profile:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --profile work\camoufox\case001\profile https://example.com
```

Benefits:

- Cookies do not leak across tasks.
- localStorage and sessionStorage stay isolated.
- Cache and Service Workers do not pollute later analysis.
- The full profile can be copied or removed for reproducibility.

### 4.2 Baseline Profiles

Files under `tool\camoufox_browser\Profiles` are baseline state. The AI may read them, but MUST NOT write business cookies, login state, or debug cache there by default.

If an existing profile must be reused, copy it first:

```powershell
Copy-Item tool\camoufox_browser\Profiles\is7lfki9.default-default work\camoufox\case001\profile -Recurse
```

Use only the copied profile.

### 4.3 Profile Cleanup

If the profile is temporary:

```powershell
Remove-Item work\camoufox\case001\profile -Recurse -Force
```

If it must be retained, record in `notes.md`:

- Profile path.
- Target domain.
- Collection time.
- Retention reason.
- Related evidence files.

## 5. Configuration File Rules

### 5.1 `camoufox.cfg`

`tool\camoufox_browser\camoufox\Cache\camoufox.cfg` is the browser preference baseline. It includes remote debugging, disabled session restore, console paste support, WebRTC local IP interception, bundled fonts, Skia canvas backend, content isolation, and many de-bloat settings.

AI MUST NOT edit this file directly during normal work. For experiments, copy the runtime or record a reversible patch.

### 5.2 `properties.json`

`tool\camoufox_browser\camoufox\Cache\properties.json` lists controllable or spoofable environment fields, including:

- `navigator.*`
- `screen.*`
- `window.*`
- `headers.*`
- WebRTC IP values.
- PDF, Battery, Fonts.
- Geolocation.
- Timezone and Locale.
- AudioContext.
- WebGL and WebGL2.
- Canvas.
- Speech voices.
- Media devices.
- Addons and certificates.

The AI MUST treat this as an environment capability index, not a checklist for blind patching. First verify whether a field is read, included in a signature, or affects server response.

### 5.3 `policies.json`

`tool\camoufox_browser\camoufox\Cache\distribution\policies.json` is the enterprise policy baseline. It disables updates, telemetry, Firefox accounts, password saving, default search engine installs, and related noise.

AI MUST NOT enable automatic updates or install external extensions by default. Extension changes affect fingerprinting and reproducibility.

## 6. Standard Workflow

### 6.1 Initial Setup

Create task directories:

```powershell
New-Item -ItemType Directory -Force work\camoufox\case001\screenshots
New-Item -ItemType Directory -Force work\camoufox\case001\network
New-Item -ItemType Directory -Force work\camoufox\case001\scripts
New-Item -ItemType Directory -Force work\camoufox\case001\env
New-Item -ItemType Directory -Force work\camoufox\case001\profile
```

Run self-checks:

```powershell
Test-Path tool\camoufox_browser\camoufox\Cache\camoufox.exe
tool\camoufox_browser\camoufox\Cache\camoufox.exe --version
Get-Process | Where-Object { $_.ProcessName -match 'camoufox|firefox' }
```

If residual processes exist, determine whether they belong to the current task. Do not kill unrelated user processes.

### 6.2 Page Loading

Direct profile launch:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --profile work\camoufox\case001\profile https://example.com
```

With `camofox-mcp`:

```text
server_status
create_tab(url="https://example.com", userId="case001", viewport={width:1366,height:768})
navigate_and_snapshot(tabId="<tabId>", url="https://example.com")
screenshot(tabId="<tabId>")
```

With Reverse MCP:

```text
launch_browser(headless=false, humanize=true, block_webrtc=true)
navigate(url="https://example.com", wait_until="networkidle", collect_response_chain=true)
take_screenshot(full_page=true)
```

Record:

- Final URL.
- Page title.
- HTTP status or redirect chain.
- Screenshot path.
- Blank page, challenge page, error page, or redirect loop state.

### 6.3 Network Collection

For structured proxy capture, use mitmproxy AI CLI:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture --listen-port 8080 --jsonl work\camoufox\case001\network\flows.jsonl
```

Then route the browser through the proxy. The browser should trigger behavior; it should not be used as a long-term traffic database.

Reverse MCP network workflow:

```text
network_capture(action="start", capture_body=true)
trigger page action
list_network_requests
get_network_request(request_id=N, include_body=true)
get_request_initiator(request_id=N)
```

Save key request evidence:

- URL.
- Method.
- Status.
- Request headers.
- Query and body.
- Response headers.
- Response body sample.
- Initiator stack when available.

### 6.4 Script and Runtime Analysis

Reverse MCP script discovery:

```text
scripts(action="list")
search_code(keyword="sign")
search_code(keyword="token")
search_code(keyword="encrypt")
search_code(keyword="decrypt")
```

Save a script:

```text
scripts(action="save", url="<script_url>", save_path="work\\camoufox\\case001\\scripts\\target.js")
```

Runtime probe:

```text
evaluate_js(expression="(() => { return { href: location.href, ua: navigator.userAgent }; })()")
```

`camofox-mcp` equivalents:

```text
camofox_get_page_html(tabId="<tabId>")
camofox_query_selector(tabId="<tabId>", selector="script[src]")
camofox_evaluate_js(tabId="<tabId>", expression="(() => { return { href: location.href, ua: navigator.userAgent }; })()")
```

Always wrap `evaluate_js` or `camofox_evaluate_js` with an IIFE and return serializable values only.

### 6.5 Hooks and Instrumentation

This section applies to Reverse MCP only. `camofox-mcp` is for automation, observation, DOM extraction, downloads, and profile reuse. It does not provide JSVMP instrumentation or network initiator stack tracing.

Use presets first:

```text
inject_hook_preset(preset="xhr", persistent=true)
inject_hook_preset(preset="fetch", persistent=true)
inject_hook_preset(preset="crypto", persistent=true)
inject_hook_preset(preset="cookie", persistent=true)
inject_hook_preset(preset="websocket", persistent=true)
```

Custom hook example:

```text
hook_function(
  function_path="XMLHttpRequest.prototype.open",
  mode="trace",
  log_args=true,
  log_return=true,
  log_stack=true
)
```

Rules:

- Hooks must be installed before target scripts execute.
- For synchronously loaded SDKs, install hooks before navigation.
- If hooks are added after page load, reload or use `instrumentation(action="reload")`.
- Hook results must be validated through logs, requests, or offline samples.

### 6.6 Environment Collection

Basic environment comparison:

```text
compare_env
```

Fine-grained collection:

```text
evaluate_js(expression="(() => { return { ua: navigator.userAgent, platform: navigator.platform, languages: navigator.languages, dpr: devicePixelRatio }; })()")
```

Engine-level tracing when supported:

```text
trace_property_access(duration=10, mode="summary", collect_values=true)
```

Order:

1. Confirm which properties are read.
2. Confirm which properties affect requests, signatures, or server responses.
3. Patch only the minimum required environment.

Do not blindly patch every field listed in `properties.json`.

### 6.7 State Export

Reverse MCP state export:

```text
export_state(save_path="work\\camoufox\\case001\\state.json")
```

Restore:

```text
import_state(state_path="work\\camoufox\\case001\\state.json")
```

With `camofox-mcp`, prefer profile tools:

```text
save_profile(tabId="<tabId>", name="case001")
load_profile(tabId="<tabId>", name="case001")
list_profiles()
delete_profile(name="case001")
```

Recommended MCP profile directory:

```powershell
work\camoufox\mcp-profiles
```

## 7. Output Rules

User-facing output MUST include high-value facts, not hidden reasoning.

Include:

- Entry point or MCP tool used.
- URL opened.
- Screenshots, requests, scripts, or state files saved.
- Key requests or scripts found.
- Evidence-backed conclusions.
- Next verification step.

Do not output:

- Unsupported guesses as conclusions.
- Hidden chain-of-thought.
- Vague statements without paths or commands.
- Cookies, tokens, or credentials in public reports.

Private reasoning may be natural and investigative, but final Markdown reports should contain only auditable evidence and conclusions.

## 8. mitmproxy Integration

Capture CLI:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe
```

Tool responsibilities:

| Tool | Responsibility |
|---|---|
| Camoufox | Open pages, trigger interactions, keep a real browser environment |
| camofox-mcp | Generic AI IDE browser control, snapshots, clicks, typing, downloads, profiles |
| mitmai | Proxy capture, JSONL export, offline inspection, flow control |
| Reverse MCP | Hooks, script search, environment tracing, request initiator stacks |

Recommended proxy capture:

```powershell
tool\mitmproxy-ai-cli-windows-x86_64\mitmai.exe capture --listen-port 8080 --jsonl work\camoufox\case001\network\flows.jsonl
```

Use Camoufox with proxy settings pointing to `127.0.0.1:8080`.

Use `camofox-mcp` for ordinary browser control. Use Reverse MCP only when initiator stacks, hooks, or instrumentation are required.

## 9. Quality Control Rules

Before ending a Camoufox task, verify:

```text
[ ] Browser entry and version recorded
[ ] Isolated profile used or reuse reason documented
[ ] Final URL and screenshot recorded
[ ] Key requests saved or reproducible
[ ] Key scripts saved or URLs recorded
[ ] Cookie, storage, and state retention documented
[ ] Temporary processes closed
[ ] Temporary profile deletion or retention documented
[ ] Main steps reproducible from commands
```

Quality levels:

| Level | Standard |
|---|---|
| A | Commands, screenshots, requests, initiator stacks, script locations, reproduction steps |
| B | Commands, screenshots, requests, and script locations |
| C | Only screenshots or request list |
| D | Subjective judgment with no evidence |

The AI MUST aim for A or B. C or D may only be temporary observations.

## 10. Cleanup Rules

Close `camofox-mcp` tabs:

```text
close_tab(tabId="<tabId>")
camofox_close_session(tabId="<tabId>")
```

Close Reverse MCP browser:

```text
close_browser
```

Reset Reverse MCP residuals:

```text
reset_browser_state(clear_network_capture=true, clear_active_routes=true, clear_persistent_hooks=true)
```

Check residual browser processes:

```powershell
Get-Process | Where-Object { $_.ProcessName -match 'camoufox|firefox' }
```

Delete temporary task data only after confirming it is under `work\camoufox`:

```powershell
Remove-Item work\camoufox\case001 -Recurse -Force
```

MUST NOT delete:

```text
tool\camoufox_browser\camoufox\Cache
tool\camoufox_browser\camoufox\Cache\camoufox.exe
tool\camoufox_browser\camoufox\Cache\camoufox.cfg
tool\camoufox_browser\camoufox\Cache\properties.json
tool\camoufox_browser\camoufox\Cache\distribution\policies.json
```

## 11. Quick Command Reference

Browser version:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --version
```

Browser help:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --help
```

Open page with isolated profile:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --profile work\camoufox\case001\profile https://example.com
```

Headless screenshot:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --headless --screenshot work\camoufox\case001\screenshots\home.png --window-size 1365,768 https://example.com
```

Open DevTools:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --devtools --profile work\camoufox\case001\profile https://example.com
```

Start debugger server:

```powershell
tool\camoufox_browser\camoufox\Cache\camoufox.exe --new-instance --start-debugger-server 6000 --profile work\camoufox\case001\profile https://example.com
```

Check processes:

```powershell
Get-Process | Where-Object { $_.ProcessName -match 'camoufox|firefox' }
```

Check whether `camofox-mcp` is built:

```powershell
Test-Path tool\camoufox_browser\camofox-mcp\dist\index.js
```

Build `camofox-mcp`:

```powershell
Push-Location tool\camoufox_browser\camofox-mcp
npm install
npm run build
Pop-Location
```

Check browser service:

```powershell
Invoke-RestMethod http://localhost:9377/health
```

Start browser service:

```powershell
Start-Process -FilePath "npx" -ArgumentList @("-y", "camofox-browser@latest") -WindowStyle Hidden
```

Scan common AI IDE MCP configs:

```powershell
$candidateFiles = @(
  ".cursor\mcp.json",
  ".trae\mcp.json",
  ".codebuddy\mcp.json",
  ".vscode\mcp.json",
  "$env:USERPROFILE\.cursor\mcp.json",
  "$env:USERPROFILE\.trae\mcp.json",
  "$env:USERPROFILE\.codebuddy\mcp.json",
  "$env:USERPROFILE\.codex\config.toml",
  "$env:APPDATA\Cursor\User\mcp.json",
  "$env:APPDATA\Trae\User\mcp.json",
  "$env:APPDATA\Trae CN\User\mcp.json",
  "$env:APPDATA\CodeBuddy\User\mcp.json",
  "$env:APPDATA\CodeBuddy CN\User\mcp.json",
  "$env:APPDATA\Code\User\mcp.json",
  "$env:APPDATA\Claude\claude_desktop_config.json"
)

$candidateFiles | Where-Object { Test-Path $_ } | ForEach-Object {
  Select-String -Path $_ -Pattern @("camofox", "camofox-mcp", "CAMOFOX_URL") -SimpleMatch
}
```

## 12. Minimal AI Workflow Template

```text
Task: <target URL / analysis goal>
Working directory: work\camoufox\<task_id>

1. Self-check
   - Verify camoufox.exe exists.
   - Record --version output.
   - Check whether camofox-mcp tools are exposed.
   - If not exposed, build and register camofox-mcp in the current AI IDE.
   - Check whether camofox-browser responds on http://localhost:9377.
   - Check residual processes.

2. Start
   - Create isolated profile.
   - Prefer camofox-mcp create_tab / navigate_and_snapshot.
   - Use Reverse MCP launch_browser only for hook or reverse-engineering tasks.
   - Open target URL.

3. Collect evidence
   - Screenshot.
   - Network requests.
   - Key scripts.
   - Cookies and storage.
   - Console logs.

4. Analyze
   - Start with request identification.
   - For normal browsing, use snapshot, DOM, and structured extraction.
   - For reverse tasks, check initiator stacks.
   - Search scripts when needed.
   - Hook or instrument only when needed.

5. Finish
   - Record evidence paths.
   - Record verified conclusions.
   - Record unverified assumptions.
   - Clean temporary state.
```

## 13. AI Behavior Baseline

- MUST use relative paths for project files.
- MUST support common MCP clients including Trae, Codex, Cursor, CodeBuddy, VS Code, and Claude Desktop.
- MUST auto-detect whether `camofox-mcp` is already installed and exposed before use.
- MUST build the local MCP project and update the current IDE config if `camofox-mcp` is missing.
- MUST back up config files before editing them.
- MUST request or perform IDE restart verification after config changes.
- MUST prefer commands, MCP, and structured output.
- MUST keep profiles isolated.
- MUST record evidence paths.
- MUST clean temporary state at task end.
- MUST NOT modify browser runtime baseline files.
- MUST NOT use the browser as a long-term business runtime unless explicitly required.
- MUST NOT treat "the page looks normal" as a substitute for request, script, and state evidence.
- MUST NOT treat one successful request as a stable conclusion without a reproduction command or state file.
