---
name: openqa-svirt
description: Use ONLY when editing or developing the svirt/VMWare backend, VMFS image preparation, copying large files on ESXi, or managing ESXi worker caches.
---

# ESXi & VMware (svirt) Backend Guidelines

1. **BusyBox 32-bit non-LFS (>2 GB limit)**: ESXi BusyBox lacks Large File Support; shell redirects (`>`) and applets (`cp`, `wc`, `sha256sum`, `sha512sum`) fail fatally with `/bin/sh: File too large` (`EFBIG`) above 2 GB.
2. **Large File Copy**: Always use 64-bit `dd if=<source> of=<dest> bs=1M 2>/dev/null` instead of `cp`.
3. **Checksums**: Always use 64-bit `openssl dgst -sha256` / `-sha512` instead of `sha*sum`, parsing `SHA256(file)= <hash>` with `awk '{print $NF}'`.
4. **BusyBox `ash` EXIT Traps**: `ash` uses the `EXIT` trap's return status as the shell exit code. End every `EXIT` trap function (e.g. `_release_claim`) with `true` (or `exit 0`).
5. **SSH Command Size Limit (<8 KB)**: BusyBox `sh -c` crashes with `EFBIG` during parsing if the script string exceeds ~8192 bytes. Define top-level shell variables (`src="/long/path"`) and reference `$src` instead of interpolating long paths repeatedly.
6. **No Globs in Logs/Echo**: Never use shell globs (`*`) in `echo` or log statements on directories with multi-GB ISOs/HDDs (triggers `ash` stat/parser failures); use exact paths or variables.
7. **Worker Module Cache**: After updating `/usr/lib/os-autoinst/` Perl modules on remote workers, restart the worker service (e.g. `systemctl restart openqa-worker-auto-restart@14.service`) to clear cached bytecode.
8. **Local `isotovideo`**: From `local/` test dirs, invoke `../../isotovideo` directly so it loads modules from the working tree.
