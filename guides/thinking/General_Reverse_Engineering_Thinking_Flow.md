# General Reverse Engineering Thinking Flow

This document is not a tool list. It is a thinking flow for moving from "I have a target" to "I have a verified, reproducible conclusion." Follow it in order, but jump back whenever evidence invalidates the current path.

Core rule: identify the layer before choosing tools; form hypotheses before claiming conclusions; verify every conclusion with evidence.

---

## 0. Opening Move: Do Not Start by Hunting for Keys

When you receive a target, do not immediately search for `AES`, `key`, or `decrypt`. Pause and ask:

```text
What layer am I looking at?

Is this .NET / Mono?
Is this Unity IL2CPP?
Is this a native PE / ELF / Mach-O?
Is this Android APK / iOS IPA?
Is this Electron / WebView?
Is this a script VM?
Is this a resource package?
Or is it a mixed architecture?
```

If the layer is wrong, every later tool choice becomes noise.

Correct opening sequence:

```text
target path -> file type -> architecture layer -> runnability -> existing evidence -> initial route
```

Record first:

- Target file or directory path.
- Platform: Windows / Linux / Android / iOS / Web / Unity / Unreal / Electron.
- Goal: architecture understanding, resource extraction, script recovery, protocol analysis, key location, or report generation.
- Existing artifacts: dump, metadata, PDB, symbols, logs, packet capture, resource package, screenshots.
- Whether the target can run.
- Whether test accounts, login state, offline samples, or traffic captures exist.

Create a workspace:

```text
artifacts/raw/          original samples, read-only
artifacts/extracted/    unpacked and extracted outputs
scripts/                reproducible scripts
notes/                  analysis notes
00_inventory.md         file list, sizes, hashes, sources
```

All transformations, unpacking, decryption, and patches must write to new paths. Never overwrite the original sample.

---

## 1. First Pass: What Am I Looking At?

Start with inventory, not decompilation.

```text
list files recursively
group by extension and size
calculate hashes
identify magic bytes and headers
search for important directories and key files
```

Maintain an architecture candidate table:

| Observed signal | Possible direction | Next step |
|---|---|---|
| `.dll`, `.pdb`, `Assembly-CSharp.dll` | .NET / Unity Mono | Inspect C# with ILSpy / dnSpy |
| `GameAssembly.dll`, `global-metadata.dat`, `*_Data` | Unity IL2CPP | Build type index with Il2CppDumper |
| `.exe`, `.dll`, `.so`, `.dylib` | Native | Inspect functions, strings, imports in Ghidra / IDA |
| `.apk`, `classes.dex`, `lib/*.so` | Android | Split Java/Kotlin and native analysis with jadx / apktool / Frida |
| `.ipa`, Mach-O | iOS | Inspect ObjC/Swift/native with class-dump / Hopper / IDA |
| `app.asar`, JS bundle | Electron / WebView | Use asar, AST tooling, DevTools |
| LuaJIT / V8 / Python / Mono traces | Script VM | Hook loader or dump runtime |
| UnityFS / pak / zip / sqlite / protobuf | Resource or data layer | Start with format analysis |

The output of this pass is not a final conclusion. It is a rough map:

```text
What platform is this?
Where is the main logic?
Where are resources?
Where are scripts?
Where is networking?
At which layer could encryption happen?
```

---

## 2. Second Pass: Split Layers Before Mixing Threads

When you see "encryption", "resources", "scripts", or "network", do not merge them into one line of thought. Split the layers:

```text
file container layer
resource object layer
script buffer layer
runtime object layer
network protocol layer
server semantics layer
```

One target may process multiple layers:

```text
outer bundle is compressed
objects inside are serialized
script bytecode is encrypted again
runtime registers protocol tables
network requests are signed
```

Before each analysis step, ask:

```text
Which layer am I testing?
Can this evidence prove something about that layer?
If this layer fails, can I observe plaintext at a higher layer?
```

Do not keep pushing on the wrong layer. If the file layer stalls, move to the loader. If the loader stalls, move to the VM. If the VM stalls, inspect runtime objects. If protocol analysis stalls, return to script-level state machines.

---

## 3. Static Analysis Flow: Find Paths Before Explaining Functions

Static analysis proposes hypotheses. It does not, by itself, make claims true.

Prioritize these chains:

```text
startup chain: entry -> init manager -> SDK initialization
resource chain: manifest -> bundle map -> load asset -> cache -> patch
script chain: loader -> custom loader -> DoString / LoadBuffer / require
crypto chain: Key/IV init -> crypto API -> decrypt/decompress -> consumer
network chain: socket/websocket/http -> encode/decode -> login -> heartbeat
config chain: server list -> channel config -> version -> hot update URL
```

Stay conservative:

```text
Seeing a string does not mean the string is used.
Seeing a function name does not mean the call path is known.
Seeing AES does not mean it decrypts the target data.
Seeing a key does not mean it is the key for the current layer.
Seeing parser failure does not mean the whole package is encrypted.
```

Minimum static-location loop:

```text
key string / API
  -> xrefs
  -> callers
  -> callees
  -> argument source
  -> return-value destination
  -> whether target data passes through this path
```

Only after this loop is complete is a function explanation reliable.

---

## 4. Resource Package Flow: Ask Format First, Encryption Second

When resource parsing fails, do not immediately conclude encryption. Split the question:

```text
What is the outer format?
Is the directory table plaintext?
Are data blocks compressed?
Is metadata encrypted?
Is object content encrypted again?
At which exact layer does the parser fail?
```

Common observations:

```text
magic: UnityFS / PK / SQLite / LuaJIT / \x1bLua / JSON / protobuf
header: version, length, offset, block table
entropy: high entropy only means possible compression or encryption
alignment: AES-CBC often aligns to 16 bytes, but this alone proves nothing
known plaintext: paths, versions, JSON `{`, Lua magic, Unity SerializedFile
```

If a tool fails, lower the goal instead of trying ten more tools:

```text
export raw blocks
skip metadata parsing
save node / object data
infer content offsets from plaintext paths
test decrypt/decompress on one object
```

A minimal verification script should answer:

```text
Which block is input?
Which decompression or decryption was used?
Did the output contain the target magic?
Was failure caused by padding, key, IV, mode, or because this layer is not encrypted?
```

---

## 5. Crypto Location Flow: Many Candidates, Evidence Order Matters

Do not only search for `AES`. Cover algorithms, frameworks, and loading paths:

```text
Rijndael, CryptoStream, CreateDecryptor, TransformFinalBlock
MD5, SHA1, SHA256, HMAC, RSA, PBKDF2, Rfc2898DeriveBytes
key, iv, salt, password, cipher, decrypt, encrypt
BCryptDecrypt, CryptDecrypt, OpenSSL, mbedTLS
LZMA, LZ4, gzip, zlib, deflate, brotli
LoadFromFile, LoadFromMemory, LoadBuffer, DoString
```

Evidence strength from weak to strong:

```text
keyword hit
  < rdata / metadata candidate
  < xrefs into crypto API
  < initializer builds Key/IV
  < decrypt function arguments match sample
  < dynamic hook captures real parameters
  < small script successfully recovers target magic
```

Key verification must be scripted:

```text
input: sample ciphertext, candidate key, candidate IV, mode, padding
output: whether target magic / header / JSON / LuaJIT / Unity SerializedFile appears
record: failure reason for every attempt
```

Do not keep testing manually, and do not reject a whole route after one failure. First verify:

```text
Is the sample from the same layer?
Does it include a header?
Should it be decompressed before decryption?
Should it be decrypted before decompression?
Is key or IV derived?
Is there an extra XOR, rolling key, or table transform?
```

---

## 6. Dynamic Analysis Flow: Use Hooks to Prove Static Hypotheses

Dynamic analysis is not random hooking. Its purpose is to prove one specific hypothesis.

Hook high-level entry points first:

```text
file IO: CreateFile, ReadFile, fopen, read
resource API: AssetBundle.LoadFromFile, LoadFromMemory, custom loader
crypto API: CreateDecryptor, TransformFinalBlock, BCryptDecrypt, CryptDecrypt
script API: luaL_loadbuffer, lua_load, lua_pcall, DoString, v8::ScriptCompiler
network API: send, recv, WebSocket, HTTP client
```

If high-level symbols are unavailable, go lower:

```text
locate RVA in Ghidra / IDA
obtain runtime module base
calculate base + RVA
attach or spawn with Frida
record arguments, return values, caller address, and surrounding buffer bytes
```

Hook discipline:

```text
read only first, do not modify arguments
test one hypothesis per hook
filter small noisy buffers
avoid heavy logic inside callbacks
guard against re-entry
save and restore VM stack
record trigger count, call stack, and buffer samples
```

If a hook does not trigger, do not immediately blame static analysis. Check:

```text
Was the hook installed too late?
Was ASLR handled?
Did execution use another DLL?
Was the function inlined?
Was the data served from a higher-level cache?
Did the target action actually run?
```

---

## 7. Script VM Flow: If the File Layer Stalls, Inspect Runtime

When file-layer keys are hard to find, or resource-layer analysis keeps looping, move to runtime.

Typical route:

```text
hook script loading entry
dump already-decrypted buffers
capture VM state pointer
traverse globals, module tables, loaded tables
dump function list, paths, upvalues, bytecode
recover protocol tables, config tables, and state machines from runtime objects
```

Lua / LuaJIT route:

```text
locate xlua / lua / luajit library
enumerate exports: lua_gettop, lua_settop, lua_next, lua_type, lua_dump
hook high-frequency APIs to capture lua_State
traverse _G and package.loaded
save function path index
then study GCfunc / GCproto / bytecode dumping
```

LuaJIT requires caution:

```text
GCRef may be a compressed pointer.
Structure layout depends on platform bitness.
GC may invalidate objects.
Probe with small samples before full traversal.
```

The goal of VM work is not "dump everything". The goal is the shortest evidence path:

```text
Which script is loaded?
Does the buffer change before and after loading?
How do script names map to module names?
Where are protocol tables registered?
When do config tables enter memory?
```

---

## 8. Network Protocol Flow: Get Semantics Before Writing a Server

If the goal is protocol compatibility, offline operation, or a mock server, do not skip client semantics.

Correct order:

```text
find protocol library: protobuf / flatbuffer / sproto / msgpack / custom binary
find send entry
find receive dispatcher
extract opcode / message id / route name
connect to script-level call sites
validate fields with traffic capture
confirm state machine
write a minimal mock server for one interface
```

Do not build a big framework first. Prove one minimal loop:

```text
client sends request
message id is known
required fields are known
response structure is known
client accepts the response and enters the next state
```

If login works but everything after it breaks, the likely problem is not framework size. Check:

```text
missing state transition fields
timestamp / session / nonce mismatch
heartbeat or reconnect semantics missing
error code does not match client expectation
script layer still performs a second validation
```

---

## 9. Jump-Back Points: When to Change Route

Reverse engineering is not linear. These signals mean you should change layer:

| Current symptom | Do not rush to conclude | More stable next step |
|---|---|---|
| High-entropy block | Definitely AES | Check compression, serialization, packed native |
| UnityPy parse failure | Whole bundle encrypted | Export raw block; separate metadata, typetree, object layer |
| AES S-Box found | Target decrypt function found | Check xrefs and whether target data passes through |
| Key string found | Target key found | Verify with sample script |
| Hook not triggered | Analysis is wrong | Check timing, ASLR, DLL, inline, trigger action |
| Function names visible | Source recovered | Still need bytecode/source dump and call path |
| File layer blocked | No way forward | Move to loader buffer or VM dump |
| Protocol fields unclear | Guess structure directly | Return to script-level message definition and state machine |

Record every jump:

```text
What was the hypothesis?
How was it tested?
What evidence failed it?
Why is the next layer more reasonable?
```

---

## 10. Evidence Recording Flow: Make Conclusions Reproducible

Every conclusion must point back to evidence.

Evidence types:

```text
file path
hash
function name
RVA / VA
string address
xrefs
call stack
hook log
buffer sample
traffic flow id
script output
screenshot
reproducible command
```

Recommended notation:

```text
[FACT] verified fact
[HYP]  current hypothesis
[TEST] validation action
[FAIL] disproven route
[TODO] next step
```

Avoid:

```text
should be AES
probably encrypted
this looks like main logic
this key should work
```

Prefer:

```text
[FACT] block_003 at offset 0x1200 decompresses with LZ4 and reveals a UnityFS header.
[FACT] sub_140123450 calls BCryptDecrypt; the third argument points to a 0x2A0-byte buffer.
[TEST] AES-CBC with candidate key A on sample_01.bin gives valid padding but no target magic.
[FAIL] outer-package full AES hypothesis disproven: directory table is plaintext and data blocks decompress with LZ4.
```

---

## 11. Minimal Delivery Flow

Every reverse engineering pass should output at least:

```text
target overview
  platform, architecture, key files

toolchain
  tools, scripts, hooks, capture method

verified facts
  evidence-backed conclusions only

key call chain
  from entry to target logic

format / compression / encryption judgment
  outer layer, inner layer, algorithm, Key/IV source, verification sample

dynamic verification result
  hook point, trigger count, arguments, sample

failed hypotheses
  which routes were disproven and why

reproduction steps
  commands, scripts, input and output paths

next steps
  sorted by expected value
```

---

## 12. Minimal Report Template

````markdown
# Reverse Analysis Report

## Target
- Path:
- Platform:
- Goal:

## Architecture Judgment
- Type:
- Key files:
- Entry:

## Verified Facts
1.
2.
3.

## Key Call Chain
```
entry -> init -> loader -> decrypt/decompress -> runtime execution
```

## Format / Compression / Encryption
- Outer format:
- Inner format:
- Algorithm:
- Key/IV source:
- Verification sample:

## Dynamic Verification
- Hook point:
- Arguments:
- Trigger count:
- Result:

## Failed Hypotheses
- Hypothesis:
- Test:
- Result:

## Reproduction Steps
1.
2.
3.

## Next Steps
1.
2.
3.
````

---

## 13. Quick Route Map

```text
If C# can be decompiled:
  inspect loader / crypto / network / script bridge first
  then dynamically verify whether data passes through the target function

If IL2CPP:
  build type index with Il2CppDumper
  inspect RVA implementation in Ghidra / IDA
  verify key function arguments with Frida

If a resource package fails to parse:
  export raw block
  identify the failing layer
  test decrypt/decompress on one object

If keys are hard to find:
  hook crypto parameters
  then hook loader buffers
  then move to script VM dump

If the file layer is blocked:
  move to runtime objects
  dump scripts, configs, and protocol tables

If building a server:
  recover protocol semantics and client state machine first
  then write a minimal mock server
```

---

## 14. One-Line Summary

Reverse engineering is not "find one suspicious point and conclude." It is:

```text
identify layer
  -> map architecture
  -> form hypothesis
  -> locate statically
  -> verify dynamically
  -> record evidence
  -> disprove wrong routes
  -> produce reproducible conclusion
```

If this chain breaks, return to the broken link and choose the next layer.

