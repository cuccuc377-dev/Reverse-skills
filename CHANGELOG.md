# Changelog

This file records notable updates to the Reverse Engineering AI Workbench.

## 2026-08-17 - Android ADB Dynamic Analysis

### Added

- Bundled Android SDK Platform-Tools revision 37.0.1 under `tool/platform-tools`.
- Added the `android-dynamic-analysis` task lane to the project skill.
- Added `guides/Android_ADB_Usage_Rules.md` with evidence-first workflows for:
  - Device authorization, serial selection, and baseline collection.
  - Package, component, process, permission, and runtime-state inspection.
  - Logcat, dumpsys, screenshots, UI hierarchy, and installed APK collection.
  - Application sandbox checks, ADB forwarding/reverse mappings, and JDWP debugging.
  - Wireless ADB, troubleshooting, evidence handling, and cleanup.
- Added a coordinated Android workflow combining ADB with Ghidra static analysis and mitmproxy traffic capture.

### Changed

- Updated the tool-selection, runtime, workspace, evidence, safety, and output rules in `SKILL.md` for Android targets.
- Updated `README.md` with the Android analysis lane, repository layout, runtime checks, requirements, and quick-start commands.
- Updated `THIRD_PARTY_NOTICES.md` with Android SDK Platform-Tools licensing and trademark information.

### Verified

- Validated `SKILL.md` with the skill-creator validation script.
- Confirmed the bundled ADB runtime reports version `37.0.1-15733141`.
- Checked Markdown code fences, trailing whitespace, referenced paths, and Git diff formatting.
