# Ghidra AI CLI

This directory adds a command-line layer on top of Ghidra headless mode. It does not replace or modify the GUI, but it exposes a large part of the usual workflow as command input/output that returns JSON.

## Files

- `ghidra_ai_cli.py` - Python wrapper around `analyzeHeadless`
- `scripts/AiCommandScript.java` - Ghidra headless script that executes commands inside the open Program

## Requirements

- A working Ghidra checkout or distribution
- Java configured as required by Ghidra
- Python 3.9+

The wrapper locates Ghidra in this order:

1. `--ghidra <path>`
2. `GHIDRA_HOME`
3. parent of this `ai_cli` directory

Both source-tree layouts and release layouts are supported:

- `Ghidra/RuntimeScripts/support/analyzeHeadless(.bat)`
- `support/analyzeHeadless(.bat)`

## Quick Start

Run a one-shot summary against a binary:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py one-shot `
  --binary sample\app.exe `
  --cmd summary
```

Create or update a persistent project:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py import `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --binary sample\app.exe `
  --overwrite `
  --cmd summary
```

Run a command against an existing imported program:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --process app.exe `
  --cmd list-functions `
  --limit 50
```

## Commands

All commands output JSON.
Passing `--output <path>` writes the same JSON result to a file as well as stdout.

| Command | Required args | Optional args | Purpose |
|---|---|---|---|
| `summary` | none | none | Program metadata, memory blocks, counts |
| `list-functions` | none | `--filter`, `--limit`, `--offset` | List functions |
| `function-info` | `--name` or `--address` | none | One function snapshot |
| `list-variables` | `--function` | `--var-kind` | Parameters, locals, return |
| `decompile` | `--name` or `--address` | `--timeout` | Decompile one function |
| `disassemble` | `--address` or `--name` | `--limit` | Disassemble from address or function |
| `xrefs-to` | `--address` | `--limit` | References to address |
| `xrefs-from` | `--address` | `--limit` | References from address |
| `callers` | `--name` or `--address` | none | Functions that call the target |
| `callees` | `--name` or `--address` | none | Functions called by the target |
| `call-graph` | `--name` or `--address` | `--depth`, `--limit` | Small call graph |
| `strings` | none | `--filter`, `--min`, `--limit` | Defined strings |
| `symbols` | none | `--filter`, `--limit`, `--offset` | Symbols |
| `imports` | none | `--filter`, `--limit`, `--offset` | External symbols |
| `search-bytes` | `--hex` | `--address`, `--end`, `--limit` | Search bytes |
| `read-memory` | `--address` | `--length` | Read bytes |
| `rename-function` | `--name` or `--address`, `--new-name` | none | Rename a function |
| `rename-symbol` | `--name` or `--address`, `--new-name` | none | Rename a symbol |
| `create-label` | `--address`, `--label` | `--primary` | Create a label |
| `delete-symbol` | `--name` or `--address` | none | Delete a symbol |
| `set-comment` | `--address` or `--function` | `--comment-type`, `--clear` | Set or clear comments |
| `set-function-signature` | `--name` or `--address`, `--signature` | `--rename`, `--preserve-calling-convention` | Apply signature |
| `set-return-type` | `--name` or `--address`, `--type` | none | Change return type |
| `set-calling-convention` | `--name` or `--address`, `--calling-convention` | none | Change calling convention |
| `set-function-flag` | `--name` or `--address`, `--flag` | `--enabled` | Toggle noreturn/inline/varargs/custom storage |
| `set-variable-type` | `--function`, `--var` or `--index`, `--type` | `--var-kind`, `--force`, `--align` | Change variable type |
| `rename-variable` | `--function`, `--var` or `--index`, `--new-name` | `--var-kind` | Rename variable |
| `set-variable-comment` | `--function`, `--var` or `--index`, `--comment` | `--var-kind` | Set variable comment |
| `create-struct` | `--struct-name`, `--fields` | `--category`, `--size` | Create a structure type |
| `apply-type` | `--address`, `--type` | `--length`, `--clear-mode` | Apply a type to memory |
| `patch-bytes` | `--address`, `--bytes` | none | Write raw bytes |
| `assemble` | `--address`, `--assembly` | none | Assemble instructions |
| `create-function` | `--entry`, `--name` | `--body-start`, `--body-end` | Create a function |
| `remove-function` | `--name` or `--address` | none | Delete a function |
| `clear-listing` | `--address` | `--end`, `--clear-context` | Clear code/data |
| `disassemble-at` | `--address` | none | Disassemble one address |
| `analysis-options` | none | `--filter` | List analysis settings |
| `set-analysis-option` | `--analysis-option`, `--analysis-value` | none | Change one analysis setting |
| `run-analysis` | none | `--changes-only` | Run auto-analysis |
| `save` | none | `--comment` | Save the program |
| `export-c` | none | `--filter`, `--limit`, `--timeout` | Export decompiled C |
| `export-functions-json` | none | same as `list-functions` | Export function list |
| `export-strings-json` | none | same as `strings` | Export strings |
| `export-report` | none | `--filter`, `--limit` | Combined report |

Command names may use hyphen or underscore.

## Examples

Find functions matching `decrypt`:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --process app.exe `
  --cmd list-functions `
  --filter decrypt `
  --limit 100
```

Decompile by address:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --process app.exe `
  --cmd decompile `
  --address 0x140012340 `
  --timeout 60
```

Find xrefs to an address:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --process app.exe `
  --cmd xrefs-to `
  --address 0x140012340
```

Search for AES S-Box prefix:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --process app.exe `
  --cmd search-bytes `
  --hex "63 7C 77 7B F2 6B 6F C5" `
  --limit 20
```

Read memory bytes:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --process app.exe `
  --cmd read-memory `
  --address 0x140000000 `
  --length 64
```

## Extra Script Arguments

Pass raw key/value arguments directly to the Ghidra script when you need an option not exposed by the wrapper:

```powershell
py -3 tool\ghidra_12.2_DEV\ai_cli\ghidra_ai_cli.py run `
  --project-dir work\ghidra_projects `
  --project-name sample `
  --process app.exe `
  --cmd disassemble `
  --address 0x140012340 `
  --script-arg address_only=true
```

## Field Format

`create-struct` accepts each field as one `;`-separated item.

Supported forms:

- `offset:type:name`
- `offset:type:name:length`
- `offset:type:name:length:comment`
- `type:name`
- `type:name:length`
- `type name`

Examples:

```powershell
--fields "0:uint32_t:magic;4:char[16]:name;20:uint8_t:flags"
```

## Notes

- GUI-only Ghidra scripts that call `askFile`, `askChoice`, `popup`, or rely on `currentAddress` should be converted to command arguments before use in this flow.
- Query commands use `-noanalysis` by default in `run` mode. Use `--analyze` if you want Ghidra analysis to run before the command.
- Import and one-shot modes run analysis unless `--no-analysis` is passed.
- Use persistent projects for large binaries. One-shot mode is convenient but repeats import and analysis each run.
