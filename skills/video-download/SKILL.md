---
name: video-download
description: Use when downloading a video from a Vimeo review/share link, when yt-dlp reports a login-required site, or when a signed site manifest has to be handed to yt-dlp's generic extractor.
---

# Video downloads

- **Vimeo review link (`vimeo.com/reviews/<token>/videos/<id>`)**: run `~/bin/vimeo-review-dl <url> [outdir]` (default `~/Downloads`; `LIST=1` probes formats, `FMT=<ids>` picks a rung). Plain yt-dlp fails: the vimeo extractor maps review URLs to the bare video id, its `web` API client is `REQUIRES_AUTH`, and it has no dpc/review handling. `--cookies-from-browser firefox` also fails without a session cookie — check the Firefox `moz_cookies` table for a `.vimeo.com` `vimeo` row, not just `vuid`/`cf_clearance`.
- **Manual recipe** (script internals): render the review page headlessly, pull the signed `player.vimeo.com/video/<id>/config` URL out of the dumped DOM (JS escapes `&` as `\u0026`), fetch that JSON, take `request.files.hls.cdns.fastly_skyfire.url`, then `yt-dlp -f bestvideo+bestaudio/best --merge-output-format mp4 --referer https://player.vimeo.com/ <m3u8>`.
- **Headless render**: `chromium --headless=new --disable-gpu --no-sandbox --dump-dom --virtual-time-budget=15000 --user-data-dir=$(mktemp -d) <url>`. The isolated `--user-data-dir` is mandatory — without it the dump attaches to the user's running browser instance and hangs until the timeout.
- **Signed CDN URLs expire** (`exp=<unix>`, ≈7 h): rerun to refresh them, never reuse a manifest from an earlier run.
- **Title metadata**: the generic extractor reports `title=NA` for a bare manifest. `--parse-metadata LITERAL:%(title)s` only assigns the literal when it contains whitespace (otherwise the literal is read as `%(field)s` and yields NA), so write the title with a lossless remux: `ffmpeg -c copy -metadata title=…`.
- **Compression recipe**: `ffmpeg -i in.mp4 -c:v libsvtav1 -crf 32 -preset 7 -svtav1-params tune=0 -c:a libopus -b:a 96k -metadata title=… -movflags +faststart out.mp4` measured 1.07 Mbps on 1080p25 seminar footage (3.54 Mbps source) → 3.3× smaller at 1.48× realtime on 16 cores. AV1 encode is CPU-only on the AMD 780M (RDNA3 decodes AV1, does not encode it). Verify with a full `ffmpeg -f null -` decode pass and keep the original file.
- **Decoder reach**: AV1 in MP4 needs a modern player; pre-2020 hardware lacks AV1 hardware decode and software 1080p AV1 decode is heavy, so use `-c:v libvpx-vp9 -crf 40 -b:v 0` for wider device support at a similar size.
- **yt-dlp 2026.08 flags**: `--no-clobber` and `--print-fragments` do not exist, and skipping existing files is already the default. Merged format ids carry the cdn suffix (`383+audio-low-Original`), so probe with `-F` before selecting a rung.
