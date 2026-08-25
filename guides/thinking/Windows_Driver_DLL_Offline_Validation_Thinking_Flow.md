# Windows Driver and DLL Offline Validation Thinking Flow

This document is not a patch recipe or a tool list. It is a thinking flow for authorized software compatibility research, offline validation migration, driver communication analysis, and failure diagnosis.

Core rule: separate the driver, device, application, authorization, and network layers before choosing an intervention point. Form hypotheses before changing behavior, preserve the original sample, and do not call a build final until an end-to-end test succeeds.

> Use this workflow only on software and systems you own or are explicitly authorized to analyze and modify.

---

## 0. Opening Move: Do Not Patch the Validation Branch First

When you receive a deployment package, do not immediately search for `key`, `login`, `heartbeat`, or a conditional jump to patch. Pause and ask:

```text
Which layers are present?

Does the host side install a kernel driver?
Does the client side contain the user-facing application?
Which DLL implements device communication?
Do authorization and device initialization share a module?
Is each network connection a LAN data channel or an Internet authorization channel?
Does the driver use an embedded signature or a signed catalog?
Is the target packed, virtualized, self-checking, or protected against runtime writes?
```

Correct opening sequence:

```text
target directory
  -> inventory and hashes
  -> module roles
  -> call graph and network boundaries
  -> authorization boundary
  -> runnability and risk
  -> initial analysis route
```

Record first:

- Original package path and source.
- Operating system, architecture, and driver type.
- Host, client, and device roles.
- Goal: architecture mapping, communication diagnosis, authorized offline migration, or report generation.
- Scope of authorization and allowed test actions.
- Whether a known-good original build exists as a baseline.
- Available logs, configuration files, captures, dumps, and successful test results.

Create an isolated workspace:

```text
artifacts/raw/          original files, preserved read-only
artifacts/baseline/     known-good baseline
artifacts/candidates/   one directory per candidate build
artifacts/logs/         application logs, event logs, captures, and dumps
scripts/                reproducible inspection and verification scripts
notes/                  hypotheses, facts, and failure records
00_inventory.md         paths, roles, sizes, hashes, versions, and signatures
```

Write every transformation to a new path. Never overwrite the original package, and never load an unknown driver or protected DLL on a daily-use host merely to see what happens.

---

## 1. First Pass: Determine What Every File Does

Start with inventory and dependencies, not decompilation.

```text
list files recursively
calculate SHA-256 hashes
identify PE type, architecture, and subsystem
inspect imports, exports, signatures, and version metadata
read INF, INI, JSON, BAT, CMD, and PowerShell configuration
map executable entry points and DLL loading relationships
```

Maintain a module-role table:

| Observed signal | Possible role | Next step |
|---|---|---|
| `.sys` + `.inf` + `.cat` | Windows driver package | Validate catalog signature, INF declarations, and file hashes |
| Main program imports `vmm.dll` | High-level memory/process API | Trace VMM calls into the device layer |
| Exports such as `LcCreate` or `LcCommand` | LeechCore-style device layer | Map device creation, commands, reads, and shutdown |
| WinHTTP imports, authorization URLs, or key fields | Possible remote authorization | Trace callers and consumers of the result |
| WSK, sockets, or a fixed LAN port | Possible device data channel | Analyze separately from Internet authorization |
| `FTD3XX.dll` | Optional FTDI/FPGA compatibility | Verify whether the active device route imports it |
| High-entropy code, virtualization, or page-protection failures | Protection or anti-tamper layer | Reduce runtime risk and favor boundary analysis |

The output of the first pass is an architecture map, not a patch offset:

```text
Where is the application entry point?
Which module creates the device?
Which module reads configuration?
Which module connects to the LAN?
Which module connects to the Internet?
Where does authorization state affect the device handle?
Which files are optional compatibility components?
```

---

## 2. Second Pass: Separate Five Independent Chains

Do not treat networking, authorization, initialization, and reading as one problem. Split at least these chains:

```text
driver installation and signature chain
host-client LAN communication chain
device initialization chain
remote authorization and heartbeat chain
application read and benchmark chain
```

A typical call path may look like:

```text
benchmark application
  -> high-level memory API
  -> device abstraction
  -> authorization initialization
  -> LAN device creation
  -> driver service
  -> physical-memory read
```

Keep the success conditions separate:

```text
authorization initialization succeeded
  != device creation succeeded
  != LAN protocol handshake succeeded
  != memory read succeeded
  != benchmark remained stable
```

Before every diagnostic step, ask:

```text
At which layer does the current failure occur?
Can the current evidence prove a fact about that layer?
Is there a known-good build for comparison?
Did the modification remove an initialization side effect required by a later layer?
```

---

## 3. Static Analysis Flow: Locate Paths Before Explaining Functions

Static analysis proposes hypotheses. It does not prove that a candidate build works.

Prioritize these paths:

```text
load chain: EXE -> high-level DLL -> device DLL -> original core
configuration chain: INI -> IP/port/device type -> device parameters
authorization chain: configuration -> login -> token -> heartbeat -> state update
device chain: device selection -> context creation -> handshake -> returned handle
read chain: application request -> VMM -> device core -> network/driver -> data
shutdown chain: heartbeat stop -> handle release -> DLL unload
```

Minimum static-location loop:

```text
string, import, or export
  -> cross-references
  -> callers
  -> callees
  -> argument source
  -> return-value destination
  -> state or handle affected on failure
```

Stay conservative:

```text
Seeing CardKey does not prove that the complete authorization entry was found.
Seeing WinHTTP does not prove that the connection performs authorization.
Seeing a socket does not prove that it carries device data.
Seeing a success branch does not prove that skipping the function preserves initialization.
Matching exports does not prove matching runtime behavior.
A DLL loading successfully does not prove that a device can be created.
A nonzero device handle does not prove that real reads succeed.
```

---

## 4. Driver Signature Flow: Distinguish File and Package Signatures

For a Windows driver package, inspect at least:

```text
whether the SYS has an embedded signature
whether the INF declares CatalogFile
whether the CAT covers the INF and SYS hashes
the signature publisher
the issuing CA and trust chain
the trusted timestamp
kernel-policy verification results
Secure Boot and Windows-version requirements
```

Keep these identities separate:

| Field | Meaning |
|---|---|
| Driver product vendor | Entity claiming to develop or supply the driver |
| Digital-signature publisher | Entity responsible for the binary or catalog signature |
| Issuing CA | Entity issuing the publisher certificate |
| Microsoft Hardware Publisher | Microsoft driver publication/signing path, not proof that Microsoft wrote the code |
| Catalog signature | Signature protecting the hashes of package files such as INF and SYS |
| Timestamp | Evidence that signing occurred while the signing certificate was valid |

Critical rule:

```text
If a catalog protects the SYS or INF, changing either file breaks the catalog hash relationship.
Do not modify a signed driver package unless the task requires it and a legitimate re-signing path exists.
```

---

## 5. Authorization Boundary Flow: Find the Concentration Point

An authorized offline-validation migration should first answer:

```text
Is authorization concentrated in one module?
Does the main executable perform a second validation?
Does heartbeat failure destroy or invalidate the device handle?
Does the login routine also construct required device state?
Which global objects, threads, callbacks, or contexts must exist after initialization?
```

Evidence strength from weak to strong:

```text
key or URL string
  < network API import
  < cross-reference into an authorization function
  < authorization result entering a state machine
  < baseline logs showing the real call order
  < device creation and real reads succeeding offline
```

Prefer a stable compatibility boundary:

```text
preserve the original device core
preserve required initialization side effects
replace only the validation decision covered by the authorized migration
preserve exports, calling conventions, parameters, and return semantics
```

Making one branch return success is not the same as completing an offline-validation migration.

---

## 6. Compatibility-Layer Flow: Interface Equality Is Only the Start

When using an adapter or proxy layer, verify all of the following:

```text
export names and ordinals
x86/x64 architecture
calling conventions
structure layout and alignment
argument forwarding
error-code semantics
thread safety
initialization order
resource-release order
recursive loading and DLL search paths
```

A common architecture is:

```text
application
  -> compatibility layer under the expected name
  -> renamed, preserved original core
```

This design still requires checks for:

- The compatibility layer loading itself again under the original name.
- An import-table change altering initialization order.
- Forwarded exports missing TLS callbacks, global constructors, or registration side effects.
- An authorization change accidentally skipping the entire initialization path.
- A candidate being declared compatible based only on hashes, imports, and exports.

---

## 7. Dynamic Verification Flow: Test One Hypothesis in Isolation

Dynamic analysis should prove a specific hypothesis. It should not begin with an unplanned `LoadLibrary` experiment.

Recommended environment:

```text
dedicated test machine or suitable virtual machine
snapshot or full rollback capability
isolated network
baseline and candidate directories side by side
kernel and user-mode dumps enabled
driver, service, and filter state recorded before testing
```

Do not treat these as lightweight checks:

```text
loading a protected DLL through ctypes.WinDLL or LoadLibrary on a daily-use host
triggering full initialization from an unknown DllMain
installing a kernel driver without rollback capability
reproducing a system crash repeatedly without collecting a dump
```

Verify from low risk to high risk:

```text
PE structure and hashes
  -> imports and exports
  -> static call paths
  -> process startup in isolation
  -> device initialization
  -> LAN handshake
  -> one read
  -> scatter reads and benchmark
  -> offline, reconnect, and long-duration stability
```

Proceed to the next level only after the current one passes.

---

## 8. Logging Flow: Make Failure Stages Observable

A compatibility layer should log stages without recording credentials:

```text
original_load=success|failed
config_load=success|failed
validation_mode=remote|offline
device_init=entered|returned
device_handle=zero|nonzero
network_connect=success|failed
read_call=success|failed
shutdown=success|failed
```

Each failure record should include:

```text
stage name
Win32, NTSTATUS, or library error code
target module and version hash
baseline or candidate identity
invocation count
relevant returned state
```

Do not log:

- License keys, session tokens, or account credentials.
- Complete hardware identifiers.
- Unnecessary physical-memory contents.
- Remote-control or access information.

Logs should distinguish:

```text
original core failed to load
compatibility layer was not entered
required initialization was skipped
device handle creation failed
network handshake failed
read call failed
read succeeded but benchmark accounting failed
```

---

## 9. Network Diagnosis Flow: Ping, TCP, and Protocol Handshake Differ

Correct order:

```text
verify IP address, mask, and route
  -> verify ARP and MAC identity
  -> test bidirectional ping
  -> test TCP reachability
  -> test application handshake
  -> test device initialization
  -> test a real read
```

Interpret evidence carefully:

| Result | What it proves | What it does not prove |
|---|---|---|
| ARP is reachable | Layer-2 neighbor resolution works | ICMP, TCP, or the application protocol works |
| One-way ping works | One outbound and one inbound ICMP path work | Both hosts accept inbound ICMP |
| TCP connects | The three-way handshake succeeds | The device protocol handshake succeeds |
| Device initialization succeeds | A device context was created | Real memory reads are correct |
| One read succeeds | The basic data path works | Scatter, benchmark, and long-term stability work |

If the host running the same client locally produces the same device-initialization error, reduce the priority of client networking and firewall theories. Investigate the protocol and initialization path after the driver accepts the connection.

---

## 10. Failed-Build Review: Version Numbers Are Not Evidence

Typical failure routes and lessons:

| Failure pattern | Surface symptom | General lesson |
|---|---|---|
| Force a success return | DLL loads but device is unusable | The routine may perform required initialization |
| Same-name proxy | Zero reads or recursive loading | Audit DLL search and the actual load target |
| Redirect an upper-layer import | Interfaces exist but behavior changes | Redirection may alter timing and side effects |
| Skip the full initializer | Success message with a null handle | UI success cannot replace device state |
| Write to protected code pages | Access denied or NTSTATUS failure | Protected modules may reject runtime code writes |
| Declare success after static checks | Real test fails | Static consistency is not end-to-end verification |
| Load a target directly on the host | Crash or system failure | Unknown initialization belongs in isolation |

Use explicit candidate states:

```text
draft       design only
static-ok   static structure checks passed
loads       loads in the isolated environment
init-ok     device initialization passed
read-ok     at least one real read passed
verified    complete target scenario passed
failed      evidence disproved the route
```

Only `verified` is eligible to be called a final candidate.

---

## 11. Jump-Back Points: When to Change Route

| Current symptom | Do not rush to conclude | More stable next step |
|---|---|---|
| All exports match | Runtime behavior matches | Verify initialization side effects and real reads |
| Login returns success | Offline migration is complete | Inspect global state, threads, and device handles |
| Ping succeeds | Application communication works | Test TCP and protocol handshake |
| TCP connects | Device service works | Validate application handshake and return codes |
| Benchmark reports zero | The network is broken | Separate null handle, read failure, and accounting failure |
| Protected-page write fails | Try more memory-protection APIs | Stop runtime patch stacking and return to a stable boundary |
| Baseline works, candidate fails | The environment is wrong | Compare the unique changes and initialization order |
| Static path looks correct, runtime fails | The operator made a mistake | Mark the hypothesis failed and return to evidence |

Record every jump:

```text
[HYP]  What is the current hypothesis?
[TEST] How was it tested?
[FACT] What was actually observed?
[FAIL] Which conclusion was disproved?
[NEXT] Why is the next route more reasonable?
```

---

## 12. Evidence Recording Flow: Turn Plausibility into Reproduction

Every conclusion should reference evidence such as:

```text
file path and SHA-256
PE architecture, imports, and exports
signature chain and timestamp
function name, RVA, and cross-references
configuration-field source
network destination and port
call-order log
Win32 error or NTSTATUS
device-handle state
single-read result
benchmark and stability result
crash dump
```

Recommended notation:

```text
[FACT] verified fact
[HYP]  current hypothesis
[TEST] validation action
[FAIL] disproved route
[RISK] dynamic-test risk
[TODO] next step
```

Avoid:

```text
Only this DLL should need changing.
The port is reachable, so everything is fine.
The exports match, so behavior is unchanged.
This is now the final build.
The crash is probably unrelated.
```

Prefer:

```text
[FACT] The baseline reads successfully in the same environment; the candidate returns a null handle.
[FACT] The runtime page-protection change returned Access Denied, so the candidate modification was not applied.
[FAIL] The hypothesis that changing only the validation return preserves device initialization was disproved.
[TEST] Preserve the original device-initialization path and move the authorized validation decision to a stable interface boundary.
```

---

## 13. Minimal Delivery Flow

Every analysis pass should produce at least:

```text
target overview
  host, client, driver, application, and device layer

file inventory
  path, role, architecture, hash, version, and signature

call graph
  application entry through the real read path

network boundaries
  LAN device communication and Internet authorization described separately

verified facts
  evidence-backed conclusions only

candidate status
  static-ok / loads / init-ok / read-ok / verified

failed hypotheses
  failed build, evidence, and reason

reproduction steps
  environment, inputs, action order, and expected output

rollback method
  originals, driver recovery, and snapshot location

next steps
  ordered by evidence value and risk
```

---

## 14. Minimal Report Template

````markdown
# Windows Driver and DLL Analysis Report

## Target
- Original path:
- Platform and architecture:
- Host/client roles:
- Goal:
- Authorization scope:

## File Inventory
| File | Role | SHA-256 | Signature | Status |
|---|---|---|---|---|

## Architecture Judgment
```text
application -> high-level API -> device layer -> driver/network -> data source
```

## Network Boundaries
- LAN device channel:
- Remote authorization channel:
- Configuration source:

## Verified Facts
1.
2.
3.

## Key Call Chain
```text
entry -> configuration -> authorization -> device init -> read -> shutdown
```

## Dynamic Verification
- Environment:
- Baseline result:
- Candidate result:
- Device handle:
- Single read:
- Scatter read / benchmark:

## Failed Hypotheses
- Hypothesis:
- Test:
- Evidence:
- Conclusion:

## Risk and Rollback
- Original files:
- Driver recovery method:
- Snapshot or backup:
- Known risks:

## Next Steps
1.
2.
3.
````

---

## 15. Quick Route Map

```text
If the package contains SYS + INF + CAT:
  validate catalog coverage and file hashes first
  do not modify the signed driver by default

If authorization and device logic share one DLL:
  map the call path and required initialization side effects
  then choose a stable compatibility boundary

If the baseline reads and the candidate reports zero:
  compare the device handle, call order, and unique changes
  do not blame the physical link first

If ping succeeds but the device fails:
  continue with TCP, protocol handshake, and device return codes

If protected pages cannot be written:
  stop adding memory-protection workarounds
  return to an interface adapter or an authorized source-level migration

If every static structure check passes:
  still test loading, initialization, reading, and stability

If the target can crash the system:
  move to a dedicated test machine or suitable virtual machine
  enable dumps and prepare rollback before continuing
```

---

## 16. One-Line Summary

Windows driver and DLL offline-validation migration is not "find a validation branch and force success." It is:

```text
establish a baseline
  -> separate driver, authorization, device, application, and network layers
  -> reconstruct the real call path
  -> identify required initialization side effects
  -> choose a stable compatibility boundary
  -> verify progressively in isolation
  -> use logs to disprove wrong routes
  -> accept only real reads and end-to-end stability as success
```

If any link lacks evidence, return to that link instead of stacking another patch onto the candidate.
