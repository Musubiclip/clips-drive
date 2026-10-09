# Musubi clips to Drive

A Claude Code skill. Paste a YouTube link and get short vertical spec clips cut from it (the [Musubiclip/clips](https://github.com/Musubiclip/clips) skill, v2 design with the musubiclip.com watermark), uploaded to Musubi's Google Drive with a view only "anyone with the link" folder link.

It ends every run with:

```
Channel: <channel name>
YouTube: <channel url>
Drive: <drive link>
```

## Install

```bash
npx skills add Musubiclip/clips
npx skills add Musubiclip/clips-drive
```

## Use

```
/musubi-clips-drive https://www.youtube.com/watch?v=...
```

## Needs

- Everything [Musubiclip/clips](https://github.com/Musubiclip/clips) needs (uv, ffmpeg, yt-dlp, Node.js 22+)
- [rclone](https://rclone.org) with a remote named `mktg`:

```bash
brew install rclone                 # Mac
winget install Rclone.Rclone        # Windows, then open a new terminal
rclone config create mktg drive scope=drive
```

Sign in with a musubiclip.com account that is a member of the Musubi clips shared drive. Works the same on Mac and Windows (PowerShell).

## Before you share a clip

Watch it with sound first. Anyone with the link can view and download, so share it privately and never post it publicly.
