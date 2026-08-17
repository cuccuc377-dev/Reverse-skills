# Android ADB Usage Rules

Use these rules for authorized Android device and application dynamic analysis with the bundled Android SDK Platform-Tools runtime.

## 1. Scope And Safety

- Operate only on devices, emulators, applications, accounts, and data the user owns or is authorized to test.
- Prefer observation and task-scoped evidence collection before state-changing commands.
- Never assume the device is rooted or the target is debuggable.
- Do not unlock, flash, wipe, uninstall, clear application data, grant or revoke permissions, reboot, or change persistent settings unless the user explicitly requests the exact action.
- Treat logs, screenshots, APKs, bugreports, tokens, identifiers, and application data as potentially sensitive. Keep them under `work\adb\<task_id>` and do not commit them.

## 2. Runtime And Workspace

Resolve commands from the project root:

```powershell
$adb = (Resolve-Path "tool\platform-tools\adb.exe").Path
$taskId = "android-app-001"
$work = "work\adb\$taskId"
New-Item -ItemType Directory -Force "$work\logs", "$work\reports", "$work\screenshots", "$work\packages" | Out-Null
Test-Path $adb
Get-Content "tool\platform-tools\source.properties"
```

Run `& $adb version` when possible. If ADB cannot create its user configuration directory in a restricted environment, report that limitation and verify the bundled revision through `source.properties`; do not redirect keys into the runtime directory.

Do not write captures, keys, pulled packages, or temporary files inside `tool\platform-tools`.

## 3. Select And Qualify The Device

Start with:

```powershell
& $adb devices -l
```

Interpret state before continuing:

- `device`: transport is ready.
- `unauthorized`: ask the user to unlock the device and approve the host key prompt.
- `offline`: reconnect or restart the task-owned ADB server, then recheck.
- no row: verify USB debugging, cable/driver, wireless pairing, and the selected connection mode.

When any ambiguity exists, select one serial and use it on every device-specific command:

```powershell
$serial = "<serial>"
& $adb -s $serial get-state
& $adb -s $serial shell getprop ro.product.model
```

Do not use `-d` or `-e` as a substitute for an explicit serial in reproducible evidence.

## 4. Record A Minimal Baseline

Capture only facts relevant to the investigation:

```powershell
& $adb -s $serial shell getprop ro.build.version.release
& $adb -s $serial shell getprop ro.build.version.sdk
& $adb -s $serial shell getprop ro.product.cpu.abilist
& $adb -s $serial shell getprop ro.product.manufacturer
& $adb -s $serial shell getprop ro.product.model
& $adb -s $serial shell getprop ro.build.fingerprint
& $adb -s $serial shell getprop ro.debuggable
```

Save the selected serial and outputs in `$work\reports`. Avoid dumping all properties unless broad device configuration is necessary, because the output may contain identifying values.

## 5. Identify The Target Package And Component

Search packages without guessing:

```powershell
& $adb -s $serial shell pm list packages | Select-String "keyword"
& $adb -s $serial shell pm path <package>
& $adb -s $serial shell dumpsys package <package> > "$work\reports\package.txt"
& $adb -s $serial shell cmd package resolve-activity --brief -c android.intent.category.LAUNCHER <package>
```

Useful ownership facts include package name, version name/code, UID, install source, requested/granted permissions, APK split paths, debuggable flag, and launcher activity. Verify them from command output rather than inferring them from an icon or process label.

## 6. Reproduce Application Behavior

Prefer an explicit component when launching:

```powershell
& $adb -s $serial shell am start -W -n <package>/<activity>
& $adb -s $serial shell pidof <package>
& $adb -s $serial shell ps -A | Select-String "<package>"
```

Use `am force-stop <package>` only when a clean process start is required and it will not discard user work. Record the action. Avoid synthetic taps and text entry when the user can reproduce the behavior more safely; when automation is necessary, record screen size/orientation and every input command.

## 7. Capture Logs With A Reproduction Window

Clear logcat only when losing prior device logs is acceptable. Otherwise use a timestamp boundary.

Clean-window pattern:

```powershell
& $adb -s $serial logcat -c
# Reproduce the target behavior.
& $adb -s $serial logcat -d -v threadtime > "$work\logs\logcat.txt"
```

Focused live pattern:

```powershell
$pid = (& $adb -s $serial shell pidof -s <package>).Trim()
& $adb -s $serial logcat --pid=$pid -v threadtime
```

If `--pid` is unavailable, filter saved output locally. Keep enough surrounding lines to preserve causality. A missing log entry does not prove an operation did not occur.

For crashes or ANRs, preserve relevant `AndroidRuntime`, `DEBUG`, activity-manager, and tombstone references. Pull protected files only when access is authorized and the device permits it.

## 8. Inspect Runtime State

Use targeted `dumpsys` output:

```powershell
& $adb -s $serial shell dumpsys activity activities > "$work\reports\activities.txt"
& $adb -s $serial shell dumpsys activity services <package> > "$work\reports\services.txt"
& $adb -s $serial shell dumpsys meminfo <package> > "$work\reports\meminfo.txt"
& $adb -s $serial shell dumpsys procstats <package> > "$work\reports\procstats.txt"
& $adb -s $serial shell dumpsys window windows > "$work\reports\windows.txt"
```

Choose the narrowest service that answers the question. Correlate package, UID, PID, component, and timestamp before claiming two events belong to the same execution.

## 9. Capture Screenshots And UI Structure

```powershell
& $adb -s $serial shell screencap -p /sdcard/reverse-skill-state.png
& $adb -s $serial pull /sdcard/reverse-skill-state.png "$work\screenshots\state.png"
& $adb -s $serial shell rm /sdcard/reverse-skill-state.png
& $adb -s $serial shell uiautomator dump /sdcard/window.xml
& $adb -s $serial pull /sdcard/window.xml "$work\reports\window.xml"
& $adb -s $serial shell rm /sdcard/window.xml
```

UI hierarchy dumps can contain displayed secrets or personal data. Capture only when necessary and inspect before sharing.

## 10. Collect Installed APKs For Static Analysis

List every base and split APK path, then pull each authorized artifact:

```powershell
$paths = & $adb -s $serial shell pm path <package>
$paths | Set-Content "$work\reports\apk-paths.txt"
# For each verified package:<remote-path> line:
& $adb -s $serial pull <remote-path> "$work\packages\"
Get-FileHash "$work\packages\*" -Algorithm SHA256 |
  Format-Table -AutoSize | Out-String | Set-Content "$work\reports\apk-sha256.txt"
```

Preserve split names and hashes. Pulling installed APKs does not necessarily collect runtime data, dynamically delivered code, or native libraries extracted elsewhere; state that limitation.

## 11. Application Sandbox Access

Use `run-as` only for an authorized debuggable package:

```powershell
& $adb -s $serial shell run-as <package> id
& $adb -s $serial shell run-as <package> pwd
```

If `run-as` fails, report the exact error. Do not conclude the requested file is absent, and do not escalate to root or copy private data through unrelated backups or exploits.

## 12. Port Forwarding And Reverse Connections

Host-to-device forwarding:

```powershell
& $adb -s $serial forward tcp:<host-port> tcp:<device-port>
& $adb -s $serial forward --list
```

Device-to-host reverse mapping:

```powershell
& $adb -s $serial reverse tcp:<device-port> tcp:<host-port>
& $adb -s $serial reverse --list
```

Use task-specific ports, verify listeners, and remove only mappings created by the task:

```powershell
& $adb -s $serial forward --remove tcp:<host-port>
& $adb -s $serial reverse --remove tcp:<device-port>
```

Avoid `--remove-all` on shared devices or hosts.

## 13. JDWP Debugging

First confirm authorization and that the target exposes a JDWP process:

```powershell
& $adb -s $serial jdwp
$pid = (& $adb -s $serial shell pidof -s <package>).Trim()
& $adb -s $serial forward tcp:<host-port> jdwp:$pid
```

For an application explicitly intended to wait for a debugger:

```powershell
& $adb -s $serial shell am set-debug-app -w <package>
# Launch the verified component, attach the debugger, and reproduce.
& $adb -s $serial shell am clear-debug-app
```

Always clear debug-app state and remove the JDWP forward after the task. A package absent from `adb jdwp` may be non-debuggable, not running, not yet initialized, or hidden by platform policy.

## 14. Network Capture With mitmproxy

Use this only when the user is authorized to inspect the application's traffic.

1. Start a task-scoped mitmproxy capture and note its host IP and port.
2. Record the current proxy value:

```powershell
$oldProxy = (& $adb -s $serial shell settings get global http_proxy).Trim()
```

3. Set the temporary proxy and reproduce the behavior:

```powershell
& $adb -s $serial shell settings put global http_proxy <host-ip>:<port>
```

4. Restore the previous state exactly. Use `settings delete global http_proxy` only when the prior value was empty or `null`; otherwise write `$oldProxy` back.

Proxy configuration does not guarantee plaintext capture. Applications may ignore the system proxy, reject user-installed CAs, use certificate pinning, or use non-HTTP protocols. Report these as constraints; do not silently add bypasses.

## 15. Wireless ADB

Prefer USB for initial trust. For supported Android versions, use the device's Wireless debugging pairing flow and user-provided address:

```powershell
& $adb pair <host>:<pairing-port>
& $adb connect <host>:<adb-port>
& $adb devices -l
```

Do not expose ADB over untrusted networks. Disconnect task-created wireless transports when finished:

```powershell
& $adb disconnect <host>:<adb-port>
```

## 16. Troubleshooting

- `unauthorized`: unlock the device, approve the exact host key prompt, and rerun `devices -l`.
- `offline`: reconnect transport; use `kill-server`/`start-server` only when doing so will not disrupt unrelated ADB sessions.
- `more than one device/emulator`: add `-s <serial>` and record it.
- `no permissions` on Windows: verify the OEM USB driver, cable, USB mode, and Device Manager status.
- `run-as: package not debuggable`: continue with public ADB surfaces; do not treat it as a missing-data result.
- empty `pidof`: verify the package, launch state, secondary process names, and whether the app exited.
- restricted shell command: record the Android version, command, and exact denial; adapt to supported public interfaces.

## 17. Cleanup And Reporting

Before finishing:

- Stop live logcat or other task-owned host processes.
- Remove only task-created forward and reverse mappings.
- Clear temporary debug-app state.
- Restore the exact prior proxy setting.
- Remove temporary remote files created for screenshots or UI dumps.
- Leave the ADB server running if other sessions may use it; otherwise note whether it was stopped.
- Retain authorized evidence in `work\adb\<task_id>` and list its paths.

Report the selected serial, target package/component, relevant PID and timestamps, commands run, artifact hashes/paths, verified findings, unresolved hypotheses, access limitations, and cleanup performed.
