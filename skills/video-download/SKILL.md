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
- **yt-dlp 2026.08 flags**: `--no-clobber` and `--print-fragments` do not exist, and skipping existing files is already the default. Merged format ids carry the cdn suffix (`383+audio-low-Original`), so probe with `-F` before selecting a rung.
