---
name: openqa-svirt
description: Use ONLY when editing or developing the svirt/VMWare backend, VMFS image preparation, copying large files on ESXi, or managing ESXi worker caches.
---

# Skill: openqa-svirt

# ESXi & VMware (svirt) Development Guidelines

This skill contains critical lessons learned, platform constraints, and system administration workarounds for the ESXi/VMware (svirt) backend in os-autoinst and openQA.

## 1. BusyBox non-LFS Limitations on ESXi
ESXi uses a minimal 32-bit BusyBox user-space that lacks Large File Support (LFS). Any attempt by the shell to write or redirect (`>`) files larger than 2 GB, or use built-in shell applets like `cp` and `wc` on files larger than 2 GB, fails fatally with a `/bin/sh: File too large` error and terminates the shell script.

## 2. Copying Large Files (> 2 GB)
- **Problem**: `cp` fails at exactly 2 GB.
- **Solution**: Always use the native 64-bit `dd if=<source> of=<dest> bs=1M 2>/dev/null` which has full large file support and bypasses any busybox EFBIG restrictions.

## 3. Checksum Verification on ESXi
- **Problem**: `sha256sum`, `sha512sum`, and `wc` are 32-bit busybox applets and fail with `File too large` on any VMDK files > 2 GB.
- **Solution**: Always use `openssl dgst -sha256` / `openssl dgst -sha512` directly. OpenSSL on ESXi is a compiled 64-bit binary, runs instantly (as it uses standard fstat/metadata queries), and never triggers any `File too large` limitations.
- **Parsing**: OpenSSL prints hashes in the format `SHA256(file)= <hash>`. Parse the hash safely by grabbing the last field with `awk '{print $NF}'`.

## 4. EXIT Traps in BusyBox ash
- **Problem**: The BusyBox `ash` shell on ESXi executes `EXIT` traps, but overrides the final shell exit-code with the return status of the trap function itself. If the last statement in the trap function evaluates to false (e.g. `[ -n "$_claimed" ]`), the entire SSH command returns exit-code `1` instead of `0`.
- **Solution**: Ensure any `EXIT` trap function (like `_release_claim`) always terminates with an explicit `true` (or `exit 0`) to prevent successful runs from being falsely reported as failures.

## 5. Shell Parsing Size Limits (EFBIG)
- **Problem**: When generating shell scripts (e.g., via Perl string interpolation) to execute over SSH via `sh -c` on ESXi, you MUST keep the generated string under roughly 8 KB (8192 bytes). If the command string is too large, the minimal BusyBox interpreter immediately crashes during parsing with a fatal `/bin/sh: File too large` kernel error (EFBIG), well before any commands are executed.
- **Solution**: Never wildly interpolate absolute paths inside loops or multi-line commands. Instead, define shell variables at the top of the SSH script (e.g., `src="/long/path"`) and use those shell variables (`$src`) throughout the generated script to drastically shrink its footprint.

## 6. Unsafe Shell Globbing
- **Problem**: If you print log output using globbing (e.g., `echo "origin: /vmfs/volumes/openqa/hdd/image*"`) in a directory containing massive files (like 17 GB ISOs), BusyBox `ash` struggles to evaluate the stat/glob expansion natively, randomly causing internal parser failures.
- **Solution**: Strictly avoid interpolating shell globs (`*`) in `echo` statements or log tracing. Use exact file paths or explicitly bound shell variables instead.

## 7. Recaching Worker Modules
- After updating `/usr/lib/os-autoinst/` Perl modules on remote workers, you MUST restart the worker process (e.g. `sudo systemctl restart openqa-worker-auto-restart@14.service`) because the Perl interpreter caches compiled modules in memory.

## 8. Local Verification
- When executing `isotovideo` manually inside `local/` test directories to run against remote VMware hosts, execute the local `isotovideo` script directly (e.g. `../../isotovideo`). It automatically resolves and loads local modules from your working tree.
