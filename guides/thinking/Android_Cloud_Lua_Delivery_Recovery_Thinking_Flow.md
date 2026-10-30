# Android Cloud Lua Delivery and Recovery Thinking Flow

This guide turns an Android APK cloud Lua analysis into a reproducible technical workflow. Each stage identifies its inputs, operations, decision criteria, evidence, and next steps after a failure. It applies to authorized script recovery, client migration, and compatibility troubleshooting.

The central questions are what the server delivers, what the client does with it, when license-key validation occurs, and why a script may fail to run. A filename, function name, or single successful response cannot establish the behavior of the entire system.

This is a workflow and case review, not the complete original project or a universal decryptor. Public content excludes live service addresses, request secrets, decryption keys, license keys, tokens, signing private keys, application source code, and raw traffic. Resolve example placeholders from a sample you are authorized to analyze.

Related guidance: [General reverse-engineering workflow](General_Reverse_Engineering_Thinking_Flow.md), [Android ADB](../Android_ADB_Usage_Rules.md), [Ghidra](../Ghidra_AI_CLI_Usage_Rules.md), and [traffic analysis](../mitmproxy_AI_CLI_Usage_Rules.md).

---

## 1. Define deliverables and analysis boundaries

Separate the objectives and validate each independently:

| Objective | Minimum deliverable | What it does not establish |
|---|---|---|
| Identify cloud behavior | Call path from the request to its consumer | The server necessarily delivers executable source |
| Preserve the payload | Original response, extracted bytes, hashes, and request record | Lua has already been recovered |
| Recover source | Module boundaries, decoder, and inverse encoding checks | All source obfuscation has been removed |
| Produce readable Lua | Transformation records, original and readable copies, and syntax checks | Original developer names and the complete project have been restored |
| Change local execution | Separate builds and test records | Application behavior no longer depends on servers or plugins |
| Verify execution | Specific device, configuration, installed APK hash, and stage evidence | Every architecture and feature works |

Record sample provenance, SHA-256, package name, version, target device, authorized network request scope, and existing test status. Capturing scripts visible to a client does not grant permission to access other accounts, enumerate script IDs, or publish third-party source code.

Suggested layout:

```text
work/cloud-lua/<case-id>/
  inventory.json
  raw/                  Original APK, responses, and containers
  extracted/            DEX, ELF, and entry-point resources
  requests/             Request and response records; keep private
  lua_decrypted/        Original decrypted bytes
  lua_readable/         Readable analysis copies
  scripts/              Acquisition, decoding, transformation, verification
  builds/<build-id>/    Separate directory for each build
  logs/                 Installation and runtime logs
  reports/              Findings and validation matrix
  public/               Separately reviewed public documentation
```

Keep originals separate from analysis copies. After a failed candidate, use a new output directory rather than recursively deleting the workspace to resolve signing-output conflicts.

## 2. Map the APK by layer

Inspect these areas first:

1. Manifest: package name, launcher Activity, SDK levels, permissions, and processes.
2. Assets: entry configuration, UI, script packages, resource bundles, and cache names.
3. DEX: startup entry, downloader, cache-hit conditions, and Java/native bridges.
4. ELF: actual script loader, decoder, signature checks, and VM calls.
5. Device: installed APK, running process ABI, and caching of extracted scripts and libraries.

Record the device-supported ABIs, APK-bundled ABIs, and actual script-process ABI separately. ARM64 support on the device does not establish that the Lua engine is running an ARM64 library.

Build evidence along the call path:

```text
Launcher Activity
  -> Configuration and environment initialization
  -> Local entry point / cache selection
  -> Remote address and script ID
  -> Request and response fields
  -> Cache file
  -> Native decoder / custom loadScript
  -> Lua module loading
  -> Validation / task initialization / application behavior
```

Trace argument sources and return-value consumers before examining individual functions in depth. A call to a function named loadScript does not establish that the response contains source code; it may load an already cached module.

## 3. Determine whether the server delivers scripts or computed results

There are at least two separate questions:

- **Payload type:** source, bytecode, encrypted module container, configuration, or computed result?
- **Timing:** delivered before login, after login, or loaded from a local cache?

Use evidence to distinguish them:

| Observed evidence | Supported interpretation | Additional evidence needed |
|---|---|---|
| Decoded response reaches Lua load/loadbuffer or custom module registration | The client received executable content | Actual decoded bytes and execution entry point |
| Response is consumed only as task status, lists, numbers, or display fields | This response may contain data or results | Whether a second script request exists |
| HTTP 200 with an application-level failure field | The request reached the server | This does not establish successful script acquisition |
| Long, high-entropy text in a JSON string | Encoding or encryption may be present | Entropy alone cannot identify the algorithm |
| Cache filename ends in .zip | A naming clue only | Magic bytes, parser, and actual structure |
| Complete payload returned without a license key in the download request | This download did not require a license key as a prerequisite | This does not establish validation-free execution |

The license-key input UI may come from the APK while the validation function comes from a subsequently downloaded module. Successful validation may only update runtime state without triggering a script download.

**Historical evidence from this case:** payloads from two read responses could be recovered offline into Lua modules. Those download requests contained no license key, login token, or device identifier, and the server returned success. Validation code was present in the recovered modules. This supports the conclusion that these downloads delivered script content with separate runtime validation. It does not establish that download authorization is absent in every version or at every point in time.

## 4. Reconstruct requests within the confirmed scope

Establish the following through static analysis:

- How primary and fallback addresses are selected, including health checks.
- Whether requests use GET, form POST, or JSON POST.
- The action, script ID, capitalization, exact field spelling, and User-Agent.
- Sources of signatures, timestamps, and session tokens.
- Ordering of read, hash, version, and related requests.
- Separate handling of HTTP status and application-level success codes.
- Redirects, timeouts, proxies, compression, and caching policy.

This case used getmd5/read operations and form-encoded requests rather than JSON. Preserve field names exactly, including unconventional spellings; do not "correct" the interface when replaying a request.

Public illustration of structure only:

```text
POST https://scripts.example.invalid/<authorized-endpoint>
Content-Type: application/x-www-form-urlencoded

action=read&id=<authorized-script-id>&<key-field>=<local-secret>
```

Preserve the following for each request:

```text
request.private.json     Complete parameters; private
request.redacted.json    Shareable, redacted description
response.body            Complete body read by the client
response.parsed.json     Readable copy when parsing is possible
result.json              Status, size, hashes, timestamp, and errors
```

Observe these boundaries:

- Record whether the HTTP client automatically decompressed response.body; a client-visible body is not raw TCP bytes.
- Set connection and read timeouts and a response-size limit. A truncated or interrupted capture must not be marked complete.
- Do not disable TLS verification to conceal certificate errors. Record the actual proxy path when applicable.
- Do not automatically expand the script-ID scope or send credentials to unknown fallback domains.
- Reuse complete historical responses where available; writing documentation does not require another request to the application server.

## 5. Extract the payload without changing its bytes

If the payload is a JSON msg string:

```python
payload = response_json["msg"].encode("utf-8")
output_path.write_bytes(payload)
assert output_path.read_bytes() == payload
```

Do not format the payload, strip whitespace, normalize line endings, or include JSON quotation marks in the container. Preserve the full response body separately from the UTF-8 bytes extracted from msg.

At minimum, verify:

1. HTTP and application-level success conditions.
2. A nonempty payload with the expected structure.
3. Byte equality after writing and rereading the file.
4. A locally computed SHA-256.
5. If the interface returns an MD5, equality with the MD5 of the same payload bytes.

Matching MD5 values establish consistency with the value declared in that server response. They do not replace authentication or a digital signature.

## 6. Recognize custom containers by structure

Both cache filenames in this case ended in .zip, but the files were text-based module containers. Their logical structure was:

```text
<encrypted-module-name>:<declared-length>:<encrypted-module-body>
|
<encrypted-module-name>:<declared-length>:<encrypted-module-body>
|
...
```

Parsing workflow:

1. Preserve a hash of the entire original payload.
2. Parse using the delimiters and encodings confirmed in the loader.
3. Determine whether the length denotes characters, hexadecimal characters, or raw bytes.
4. Ignore empty segments only when the confirmed format permits them.
5. Check decoded module names for duplicate entries and unsafe paths.
6. Verify the module count and total decoded byte count.

In this case, the declared length referred to the ciphertext's hexadecimal text length. Treating it as the decrypted length would produce an incorrect conclusion. The encrypted fields used hexadecimal text and therefore did not naturally contain the pipe delimiter. Do not generalize that property to binary formats.

Treat exported module names as untrusted paths. Reject absolute paths, drive prefixes, alternate paths using backslashes, .. components, empty names, and duplicates after normalization. Confirm that every resolved output path remains under the output root.

## 7. Confirm each transformation in the loader

The data flow in this case was:

```text
Module name:
  HEX -> RC4 -> UTF-8 module name

Module content:
  HEX
    -> RC4
    -> JNI Modified UTF-8 null-character restoration
    -> Repeating XOR with script-ID bytes
    -> URL-safe Base64 decoding
    -> UTF-8 Lua source
```

The RC4 parameters came from the sample's loader, and the repeating XOR parameter came from the script ID. Do not change their byte representations merely because they look hexadecimal. For example, an ASCII string key differs from the result of applying fromhex to that string.

Verify each layer:

| Layer | Verification points |
|---|---|
| HEX | Character set, even length, and whether letter case affects comparison |
| RC4 | KSA/PRGA, actual key bytes, and whether state resets for each module |
| JNI strings | Whether C0 80 represents U+0000 and whether other nonstandard UTF-8 cases occur |
| XOR | ID encoding, starting index, and repetition period |
| Base64 | URL-safe alphabet, padding, and handling of invalid characters |
| Source | UTF-8 text, Lua bytecode, or another container layer |

The RC4 output in this case represented null characters as C0 80. This local normalization was used only after confirming that the remaining content stayed within the ASCII range produced by the subsequent Base64/XOR stages. This replacement is not a general Modified UTF-8 decoder.

Pseudocode:

```text
for each validated segment:
    name = decode_name(segment.name_hex, key_bytes)
    intermediate = rc4(hex_decode(segment.body_hex), key_bytes)
    normalized = normalize_confirmed_modified_utf8(intermediate)
    encoded = xor_repeat(normalized, script_id_bytes)
    source = strict_urlsafe_base64_decode(encoded)
    check_utf8(source)
    verify_exact_inverse(source, segment)
    write_under_output_root(name, source)
```

Pass key_bytes through private input in a real script. Do not hardcode this case's values into a public repository.

## 8. Verify decryption through inverse encoding

Recognizable Lua keywords are insufficient. For every module, perform:

```text
Source
  -> URL-safe Base64
  -> Repeating XOR
  -> Restore the JNI null-character representation
  -> RC4
  -> HEX
  -> Compare byte-for-byte with the corresponding original ciphertext
```

Also verify canonical Base64, module paths, the original container hash, and source-file hashes. If an algorithm permits equivalent encodings, state whether a comparison uses normalized values or original bytes. Do not report these different assertions interchangeably as "exact equality."

All 116 modules in this case passed exact inverse encoding checks. This establishes byte consistency of the outer recovery process; it does not prove that readability transformations or application behavior are correct.

Common failures:

| Symptom | Check first |
|---|---|
| Garbled module names | RC4 key bytes, HEX interpretation, and state resets |
| Partially incorrect content with correct names | XOR parameters, script ID, and JNI null characters |
| Invalid Base64 characters | Errors in the previous layer; do not hide them with permissive decoding |
| Readable Lua followed by truncation | Response capture, length units, and line-ending changes during text output |
| Readable plaintext that fails exact inverse encoding | Padding, encoding normalization, or modified original bytes |

## 9. Keep readability transformations separate

Maintain two outputs:

- lua_decrypted: faithful to the original recovered bytes.
- lua_readable: decoded strings, locally simplified structure, and formatting.

Record input and output hashes, counts for each transformation, and structures left unchanged.

### 9.1 String decoding

Process only decoder calls whose arguments are confirmed constants:

1. Extract the pure decoding logic and constant parameters.
2. Reimplement the algorithm independently with constrained execution.
3. Cross-check integer overflow, floating-point behavior, byte order, and modulo operations.
4. Replace only identified call expressions, preserving comments and string contents.
5. Verify that the same seed in the same module produces consistent results.
6. Preserve and report calls that cannot be decoded.

This case compared a Python implementation against an independent Lua arithmetic implementation for each call. Only reimplemented pure functions were executed, not the top-level code of downloaded modules.

### 9.2 Control-flow flattening

Transform only dispatchers proven to follow a finite, linear state sequence. Preserve:

- Branch-local variable scope.
- Bindings captured by closures.
- The scope of return and break.
- Conditional exits and side-effect ordering.

Use do ... end where necessary to retain branch-local scope. Leave dynamic state transitions, conditional branches, and loops without proven termination unchanged.

Do not extract obfuscated functions by taking everything "from one function to the next function." That region may also contain outer dispatcher assignments, elseif branches, local initialization, and decoding helpers. An intermediate attempt in this case broke syntax for exactly this reason. Use lexical or syntactic block matching, or assertion-guarded locations for a confirmed structure.

### 9.3 Unicode method names and runtime differences

The original sample contained Chinese method identifiers that standard Lua 5.3 did not accept. An analysis copy can use an equivalent string-key representation:

```lua
-- Illustration: represent an extended-syntax method name as a string key.
-- These escapes preserve the UTF-8 bytes of the example Unicode name.
local method_name = "\xE4\xB8\xAD\xE6\x96\x87\xE6\x96\xB9\xE6\xB3\x95"
Object[method_name] = function(self, value)
    return value
end
Object[method_name](Object, value)
```

Preserve the actual key bytes and self parameter, and record the changed locations. Do not modify the original decrypted copy to conceal compiler differences.

### 9.4 Syntax success does not establish execution success

Compile without calling the result:

```lua
local chunk, message = load(source, module_name, "t", {})
assert(chunk, message)
-- Do not call chunk here.
```

An empty environment table is not a sufficient sandbox for executing untrusted Lua. The constraint above depends on never calling the compiled function; compilation should also have resource limits. Run application tests only in a separately authorized, isolated environment.

## 10. Separate license validation from application dependencies

Classify behavior along the path from the main entry point to each call site. Do not delete code in bulk based on string keywords:

| Category | Examples | Main question |
|---|---|---|
| Download state | Package hash, script ID, version updates | Which bytes are loaded? |
| Authorization state | License-key login, expiry, heartbeat | Is this independent of downloading? |
| Startup state | Advertisement stage, certificate state, initialization completion | Does the engine reuse this state as an execution prerequisite? |
| Session state | Client/socket objects, device information | Is this required for later requests? |
| Functional dependencies | Game processes, memory addresses, plugins | What cannot be supplied merely by removing a prompt? |
| Communication compatibility | ping, version, UDP/TCP/UDS | Does the check represent an actual protocol capability? |

In this case, a call graph could be built from Main, LoadModule, Init, the validation-service wrapper, and the validation UI. After a module is removed, inspect initialization, exit callbacks, heartbeats, account UI, and global-variable references for remaining dependencies.

Absence of a license-key prompt does not establish absence of network activity. Endpoint discovery, plugin downloads, optional notifications, and local communication may remain.

## 11. Isolate immediate exit with a minimal script

Separate failure stages:

```text
Installation failure
  -> Application entry failure
  -> Engine not started
  -> Incorrect cache / entry point
  -> Script execution not permitted
  -> Decoding / compilation failure
  -> Module initialization failure
  -> Application dependency failure
```

Use an observable minimal script in a dedicated diagnostic build:

```lua
toast("Diagnostic entry point executed")
sleep(2500)
```

Check entry logs and elapsed time before exit, rather than relying solely on print. Standard output was redirected in this case, so missing print output did not establish that execution never occurred. Combine timing with entry evidence to distinguish script execution from loading or network waits.

After the required startup state was restored, the minimal script ran for approximately 2.59 seconds; previously it had been skipped before execution. The full script subsequently displayed its first-use information screen. These observations establish that the execution entry became reachable and that initialization reached that screen, respectively. They do not establish that later game tasks worked.

### 11.1 Advertisement flow may also initialize state

The splash flow in this case also initialized a Java state table. Jumping directly to the next Activity omitted that state. The engine's pre-Lua check failed, and the process then exited with code 0.

Consequently:

- Exit code 0 does not establish that Lua ran.
- Audit state writes before removing a UI path.
- Preserve required initialization in the fix; do not permanently replace the entire execution check with true.
- Identify the process, object, and lifecycle that own the state.

### 11.2 Re-signing can affect internal comparisons

APK installation signature verification, Java certificate-digest comparisons, and native identity checks are separate layers. Successful installation after re-signing does not establish that the application accepts its new signature internally.

For authorized local re-signing compatibility work, verify the actual signing certificate and the source of internal expected values, and record localized changes. Removing every signature check should not be the default approach, and a re-signed package must not be represented as having the original publisher's signing identity.

### 11.3 Replacement installation can retain old scripts and libraries

If flag files or cache hits cause the application to skip extraction, install -r may leave old scripts or libraries in use.

Verify each layer:

```text
SHA-256 of the APK intended for delivery
  -> SHA-256 of the APK installed on the device
  -> Version of the extracted scripts
  -> Libraries / ABI actually loaded by the process
  -> Entry logs and stage results
```

Read through authorized interfaces only. Record insufficient permissions explicitly rather than escalating privileges without authorization. Locate the relevant cache instead of clearing all application data.

## 12. Derive troubleshooting rules from observed failures

### 12.1 Missing application metadata

The original candidate-discovery function returned a message meaning "community app not detected" when discovery failed. Its caller treated that message as a package name, received nil from the metadata query, and crashed while accessing .app.

Correction principles:

- Represent no candidates as an empty list; reserve explanatory text for display.
- Fall back to displaying the real package name if its application label is unavailable.
- Keep selection entries and package-name arrays in the same order.
- Stop task creation on an empty candidate set instead of passing nil downstream.

### 12.2 Missing multi-instance number

The multi-instance mode extracted a number from the package name and used it to calculate a port. Broadening discovery to all applications introduced package names without digits. Extraction returned nil, and the subsequent "base port + instance number" calculation failed.

Do not replace a missing number with 1 or use the list position as the instance number: either approach may connect to the wrong instance.

Preserve or reconstruct an explicit "application -> instance number -> communication endpoint" mapping, and validate it before creating a task. The mere presence of digits does not prove the mapping is correct; the endpoint must also match the target implementation.

The final candidate in this case retained the original numbered-package discovery and port mapping for multi-instance mode. Single-instance mode could independently use explicit application selection. The intermediate build that broadened multi-instance discovery too far was unsuitable for delivery.

### 12.3 Removing a check does not remove its dependency

After an identity or version handshake is removed, actual tasks may still require:

- Local socket commands implemented by the other endpoint.
- Specific memory layouts.
- Plugin-provided features.
- The expected game interface and version.

State exactly which blocking check was removed. Do not describe this as compatibility with every community app.

### 12.4 Installation failure caused by an old target SDK

Another legacy APK in this case passed ZIP, alignment, and signature checks, but the device returned:

```text
INSTALL_FAILED_DEPRECATED_SDK_VERSION:
App package must target at least SDK version 19, but found 15
```

This was the threshold observed on that emulator at the time, not a universal threshold for all Android 14 systems. Preserve the complete device output and distinguish SDK restrictions from ABI incompatibility, signature conflicts, and package corruption.

The unchanged APK installed successfully on the identified emulator using a compatibility installation option for low target SDKs. Installation success still did not establish plugin or application compatibility.

## 13. Validate by stage and report the actual scope

| Level | Required evidence |
|---|---|
| L0 Original inputs | Hashes, sizes, and provenance of original packages and responses |
| L1 Format and recovery | Container parsing and inverse encoding checks for every module |
| L2 Readability transformations | Syntax checks, pure-function fixtures, and unchanged-structure records |
| L3 Packaging | Change manifest, DEX checks, ZIP integrity, alignment, and signatures |
| L4 Installation and identity | Identified device, installation result, and installed APK hash |
| L5 Entry execution | Runtime evidence from the minimal script or full entry point |
| L6 Initialization | UI, module loading, target selection, configuration, and dependencies |
| L7 Application behavior | A specific task completed and its result checked in an authorized environment |

Report the highest completed level and untested scenarios. A first-use dialog proves only that execution reached that stage. Results from non-root and root environments, different ABIs, and different modes are not interchangeable.

When a device disconnects:

1. Stop device-dependent operations; do not switch to another connected phone.
2. Complete checks that can run locally.
3. Mark the final package as not installed or not run, as applicable.
4. State which build was last left on the device.
5. After reconnection, verify the installed hash before reproducing the issue.

An intermediate package was left on the emulator during this case. Its hash differed from the final delivery package, explaining why the old multi-instance error persisted. Version verification belongs in the troubleshooting process; icons and versionName alone are insufficient.

## 14. Historical results and evidence limits

These figures come from the saved download, decryption, and transformation manifests for this case. They describe that snapshot, not the server's current state:

| Metric | Result |
|---|---:|
| Sizes of the two cache containers | 2,782,106 / 2,668,562 bytes |
| Originally recovered modules | 57 single-instance, 59 multi-instance; 116 total |
| Originally recovered source sizes | 1,031,632 / 988,105 bytes |
| Exact inverse encoding checks | 116 modules passed |
| String-decoder calls replaced in readable copies | 22,374 |
| Proven linear dispatchers simplified | 398 |
| Dispatcher structures retained | 28 across 15 files |
| Unicode method syntax compatibility rewrites | 4 |
| Lua 5.3 syntax checks on readable modules | 116 passed |

Later local builds omitted two validation modules per mode, leaving 55 + 57 = 112 embedded modules. Do not report 112 as the number originally downloaded or decrypted.

Prefer UTC for recorded timestamps and identify device, host, and report time zones. An emulator's displayed time is not the report-generation time.

Private evidence index:

| Stage | Local file types |
|---|---|
| Download | request_manifest.json, download_summary.json, response.body |
| Decryption | lua_decrypted/manifest.json |
| Readability | lua_readable/manifest.json, decoded_strings.json |
| Verification | lua_verification.json |
| Build | build_report.json / build_manifest.json, signature verification logs |
| Device | Installation output, installed APK hash, logcat, stage screenshots |

The original evidence is not published with this guide. This document summarizes the method and results; independent reproduction requires an authorized sample and the relevant private parameters.

## 15. Publication and delivery checks

Select only reviewed files for publication. Do not add the entire work/ directory to Git.

Checklist:

- [ ] Live request addresses, secrets, license keys, cookies, tokens, and device identifiers have been removed.
- [ ] No keystores, signing passwords, full traffic captures, decrypted application source, or screenshots containing personal information are included.
- [ ] Example domains and keys are clearly placeholders.
- [ ] Original source and readability copies have clearly defined roles.
- [ ] Each conclusion maps to an evidence type; historical results are not presented as guarantees about the current server.
- [ ] Signature, format, runtime, and functional validation are reported separately.
- [ ] README links resolve, code fences are complete, and files use UTF-8.
- [ ] The commit contains only this guide and necessary index changes.
- [ ] The remote branch, commit, and document content are verified after pushing.
- [ ] Private local evidence is retained, and cleanup of temporary state is recorded.

Suggested delivery summary:

```text
Completed: <acquired / recovered / made readable / verified through stage>
Input snapshot: <hashes and provenance records>
Public artifacts: <document and commit>
Private material: <keys, original payloads, application source, etc.>
Validation scope: <modes, ABIs, devices, and untested dependencies>
Current device build: <verified hash or explicit statement that it is not installed>
```
