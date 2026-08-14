# Ghidra AI CLI Usage Rules

This document defines how an AI agent should use the Ghidra command-line reverse engineering tool in this project. All paths are relative to the project root.

Current release entry point:

```powershell
tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py
```

Ghidra Headless backend:

```powershell
tool\ghidra_12.2_DEV\support\analyzeHeadless.bat
```

AI command script:

```powershell
tool\ghidra_12.2_DEV\ai_cli\scripts\AiCommandScript.java
```

## 0. Core Purpose

This tool is a JSON command bridge over Ghidra Headless. The AI MUST treat it as a repeatable, auditable, scriptable reverse engineering workbench, not as a one-shot black box.

The tool is responsible for:

- Importing binaries.
- Running Ghidra auto-analysis.
- Listing functions, symbols, strings, imports, and references.
- Decompiling, disassembling, and reading memory bytes.
- Applying project-level edits such as names, comments, types, structures, and patches.
- Returning structured JSON for automated reasoning.

The AI is responsible for:

- Verifying tool availability first.
- Importing the sample correctly.
- Building a high-level map with small read-only commands.
- Drilling into selected functions only after evidence points there.
- Binding every conclusion to command output, addresses, function names, strings, imports, xrefs, or call graph evidence.

## 1. Entry Point Rules

All commands in this document assume the current working directory is the project root, the directory that contains `SKILL.md`, `guides\`, and `tool\`. If the current directory is different, change to the project root before testing paths or running Ghidra commands.

ALWAYS use the release entry point:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py --help
```

MUST NOT default to any source tree path. Daily analysis uses `tool\ghidra_12.2_DEV`; source code is only for maintenance and rebuilding.

If `tool\ghidra-master` is present, treat it as a source or maintenance tree only. Do not infer the runtime entry point from that directory, and do not ask the user to confirm the structure unless `Test-Path tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py` fails.

If the Ghidra root must be set explicitly, use:

```powershell
--ghidra tool\ghidra_12.2_DEV
```

## 2. Reasoning and Reporting Rules

Before starting any non-trivial Ghidra analysis, the AI MUST reference and follow the general reasoning flow in:

```powershell
guides\thinking\General_Reverse_Engineering_Thinking_Flow.md
```

This reference is mandatory for internal analysis structure. It defines the broad investigation rhythm: observe, map, hypothesize, validate, correct, and report only evidence-backed conclusions.

When using this tool, the AI should reason like an investigator: observe the sample, collect leads, test hypotheses, then narrow the conclusion.

Private reasoning may contain natural transitions such as:

- Hmm, the import table suggests a GUI program, but that is not enough.
- Wait, check xrefs before assuming this is the main loop.
- Actually, this string looks like a runtime bootstrap rather than business logic.

These are private reasoning notes. The AI MUST NOT output full hidden reasoning, long chain-of-thought, or internal monologue. User-facing reports should include only:

- What commands were run.
- What evidence was found.
- What conclusion is currently supported.
- What should be checked next.

If an execution framework requires an internal `thinking` block, that block MUST stay hidden and MUST NOT appear in generated Markdown or final reports.

## 3. Standard Workflow

### 3.1 Initial Contact

After receiving a target file, first confirm that it exists:

```powershell
Get-Item FPSController.exe
```

Run a lightweight one-shot summary:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py one-shot `
  --binary FPSController.exe `
  --cmd summary `
  --no-analysis
```

Purpose:

- Confirm loader and architecture.
- Identify sections and entry points.
- Estimate function count.
- Decide whether full analysis is needed.

MUST build a target profile before decompiling individual functions.

### 3.2 Persistent Project

For large samples or multi-step work, ALWAYS use a persistent project instead of repeatedly using one-shot mode.

Recommended project directory:

```powershell
work\ghidra_projects
```

Project directory names MUST NOT start with `.`. Ghidra rejects hidden-style path elements.

Import command:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py import `
  --project-dir work\ghidra_projects `
  --project-name sample_project `
  --binary FPSController.exe `
  --cmd summary `
  --analysis-timeout 180 `
  --max-cpu 4 `
  --overwrite
```

### 3.3 Mapping Pass

After import, query the project in this order:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample_project `
  --process FPSController.exe `
  --cmd functions `
  --limit 50 `
  --read-only
```

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample_project `
  --process FPSController.exe `
  --cmd strings `
  --min 5 `
  --limit 100 `
  --read-only
```

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample_project `
  --process FPSController.exe `
  --cmd imports `
  --limit 100 `
  --read-only
```

The mapping pass should identify:

- Program type.
- Compiler or packer indicators.
- Suspicious strings.
- Entry functions.
- Important imported APIs.
- Likely main loop, unpacking, config loading, network, file, process, or UI logic.

### 3.4 Hypothesis Handling

The AI MUST keep multiple hypotheses open. Do not classify a program from one string or one import.

Examples:

- `_pyi_main_co` suggests PyInstaller, but also check Python DLLs, PYZ archive strings, bootstrap logic, and entry call chain.
- `CreateWindowExW` suggests GUI behavior, but verify window class registration and the message loop.
- `WinHttp`, `WSA`, or `InternetOpen` suggests network behavior, but verify xrefs and call arguments.

### 3.5 Deep Validation

Check xrefs before explaining important data or strings:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample_project `
  --process FPSController.exe `
  --cmd xrefs-to `
  --address 0x14002fbd8 `
  --limit 30 `
  --read-only
```

Decompile selected functions:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample_project `
  --process FPSController.exe `
  --cmd decompile `
  --entry 0x140001000 `
  --timeout 60 `
  --read-only
```

MUST confirm relationships with `xrefs-to`, `callers`, and `callees` before assigning function purpose.

## 4. Concurrency and Project Lock Rules

EXTREMELY IMPORTANT: never run multiple `run` commands against the same Ghidra project at the same time.

Ghidra projects have locks. Parallel access may cause:

- `_headless_returncode = 1`
- `Invalid JSON emitted by Ghidra script`
- Missing JSON output.
- Failed project open.

Correct behavior:

- Commands targeting the same `--project-dir` and `--project-name` MUST run sequentially.
- Ordinary file reads may run in parallel.
- Do not parallelize access to one Ghidra project.

## 5. JSON Output Rules

Normal commands return JSON. The AI MUST check:

```json
"ok": true
```

Then read:

```json
"data": {}
```

If the output contains:

```json
"ok": false
```

or:

```json
"error": "Invalid JSON emitted by Ghidra script"
```

rerun with:

```powershell
--show-log
```

Then inspect:

- `_headless_stdout`
- `_headless_stderr`
- `_headless_returncode`

Do not guess the failure cause without logs.

## 6. Analysis Depth Rules

Choose analysis depth according to task complexity.

Lightweight identification:

```powershell
--cmd summary --no-analysis
```

Normal static analysis:

```powershell
--analysis-timeout 180 --max-cpu 4
```

Higher decompiler quality:

```powershell
--analyze
```

Fast queries on an existing project:

```powershell
--read-only
```

Rules:

- Small samples may use one-shot mode.
- Large samples should use persistent projects.
- Repeated queries MUST reuse the project.
- Do not rely on `--no-analysis` when complete references, functions, and strings are required.

## 7. Editing Command Rules

Editing commands include, but are not limited to:

- `rename-function`
- `rename-symbol`
- `create-label`
- `set-comment`
- `set-function-signature`
- `set-variable-type`
- `create-struct`
- `apply-type`
- `patch-bytes`
- `assemble`
- `clear-listing`
- `remove-function`

Before any edit, the AI MUST state:

- Target address.
- Current name.
- New name or new value.
- Evidence and reason.
- Whether the project should be saved.

Read-only commands MUST use `--read-only`.

Editing commands MUST NOT use `--read-only`.

Save the project when needed:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample_project `
  --process FPSController.exe `
  --cmd save `
  --comment "AI annotations"
```

`patch-bytes` and `assemble` modify the Ghidra Program inside the project. They do not directly patch the original file on disk.

## 8. Naming and Comment Rules

Names MUST come from evidence, not intuition.

Acceptable evidence includes:

- Direct string references.
- Clear API call patterns.
- Call graph position.
- Argument behavior.
- Return value semantics.
- Known runtime library patterns.

Good names:

- `pyi_extract_archive`
- `create_main_window`
- `load_config_file`
- `dispatch_message_loop`
- `resolve_python_dll`

Bad names:

- `do_thing`
- `maybe_main`
- `important_func`
- `unknown_logic`

If evidence is weak, write a comment describing the hypothesis instead of renaming.

## 9. Decompiler Interpretation Rules

Decompiler output is not source truth. Treat Ghidra C as a structured approximation.

When explaining a function, include:

- Function entry address.
- Callers and callees.
- Important APIs.
- Important strings.
- Branch conditions.
- Data reads and writes.
- Unconfirmed points.

Do not paste a large C block and then assert a conclusion. Use short excerpts and evidence-driven explanation.

## 10. Common Command Matrix

| Goal | Command |
|---|---|
| Program overview | `summary` |
| Function list | `functions` or `list-functions` |
| Function details | `function-info` |
| Decompile | `decompile` |
| Disassemble | `disassemble` |
| Strings | `strings` |
| Symbols | `symbols` |
| Imports | `imports` |
| References | `xrefs-to` / `xrefs-from` |
| Callers | `callers` |
| Callees | `callees` |
| Small call graph | `call-graph` |
| Byte search | `search-bytes` |
| Memory read | `read-memory` |
| Report export | `export-report` |

Command names may use hyphens or underscores, for example `xrefs-to` and `xrefs_to`.

## 11. Error Handling Rules

### 11.1 Project Directory Missing

Symptom:

```text
Directory not found
```

Fix:

```powershell
New-Item -ItemType Directory -Force work\ghidra_projects
```

### 11.2 Project Path Starts With Dot

Symptom:

```text
Path element starting with '.' is not permitted
```

Fix: use a normal directory such as:

```powershell
work\ghidra_projects
```

### 11.3 No JSON Output

Rerun with:

```powershell
--show-log
```

Check for:

- Java script compilation errors.
- Project lock conflicts.
- Path mistakes.
- Ghidra loader errors.
- Analysis timeout.

### 11.4 Analysis Timeout

A timeout does not always mean import failure. Check whether valid JSON was still emitted. If more complete analysis is required, increase:

```powershell
--analysis-timeout 300
```

## 12. Cleanup Rules

Temporary tests should prefer `one-shot`; it creates and removes temporary projects automatically.

After persistent project tests, remove only project directories created for that task. Before recursive deletion, verify that the path is inside the workspace.

Recommended cleanup target:

```powershell
work\ghidra_projects
```

MUST NOT delete:

- `tool\ghidra_12.2_DEV`
- Original sample files.
- User documents.
- Directories with unclear ownership.

## 13. Final Response Rules

Final responses MUST be concise and verifiable.

Include:

- Tool entry point used.
- File analyzed.
- Key commands executed.
- Key facts found.
- Files created or changed.
- Remaining risks or incomplete checks.

Do not output:

- Hidden reasoning.
- Unsupported claims.
- Large unrelated logs.
- Unverified certainty.

Recommended final shape:

```text
Done.

I used tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py to run summary, strings, imports, and decompile on xxx.exe.
Key result: ...

Project directory: ...
The original sample was not modified.
```

## 14. Quality Gate

Before ending a task, the AI MUST verify:

- Tool entry exists.
- Commands returned JSON.
- `ok` is `true`.
- Addresses and names come from output.
- Same-project commands were not parallelized.
- Test projects were cleaned when appropriate.
- Release tool directories were not deleted.
- Final conclusions are backed by command output.

If any item fails, continue verification or clearly report the failure.

## 15. Project Baseline Command

Minimal availability test for this project:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py one-shot `
  --binary FPSController.exe `
  --cmd summary `
  --no-analysis
```

Expected shape:

```json
{
  "ok": true,
  "command": "summary",
  "_headless_returncode": 0
}
```

If this fails, do not proceed to deep analysis. Fix the tool path, Java environment, Python environment, or Ghidra release integrity first.
