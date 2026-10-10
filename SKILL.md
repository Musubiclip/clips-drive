---
name: musubi-clips-drive
description: Cut spec clips from a YouTube video with the musubi-clips skill, then upload them to Musubi's Google Drive (marketing@musubiclip.com, the "Musubi clips" shared drive) and hand back one view only "anyone with the link" folder link to send to the creator or brand. Use this whenever someone shares a YouTube link and wants clips uploaded, put on Drive, shared, or "send me the link", or asks for clips plus a Drive link, even if they never mention a skill.
---

# Musubi clips to Drive

This is the `musubi-clips` skill with one more step at the end: the finished clips go to Google Drive and the user gets a link anyone can open but nobody can edit.

## 1. Make the clips

This skill needs the `musubi-clips` skill, usually at `~/.claude/skills/musubi-clips` (on Windows `%USERPROFILE%\.claude\skills\musubi-clips`). If it is missing, ask the user to install it with `npx skills add Musubiclip/clips`.

Read `musubi-clips/SKILL.md` and follow it exactly, steps 1 to 7 (prepare, pick moments, start the video download, translate the captions into English, check subtitles, render, look at the contact sheets). Use that skill's directory as `<skill dir>` in its commands. Keep the `title` and `workdir` that `prepare` printed.

**Render with the v2 design and the musubiclip.com watermark by default**, since these clips leave Musubi:

```bash
uv run <skill dir>/scripts/clipper.py render <workdir> -n <clips wanted> --design v2 --watermark on [--keep-height 0.86] [--end-screen [LOGO]]
```

Drop the watermark (`--watermark off`) or use `--design v1` only when the user asks. Add `--end-screen` (see musubi-clips step 6) when the user wants the creator's or brand's logo at the end.

Do not upload until the contact sheets have been checked in step 7. On Windows, run the commands in PowerShell exactly as written; `uv`, `rclone` and the clipper behave the same.

## 2. Upload, share and check

One command does it on Mac and Windows alike (it needs only `uv` and `rclone`):

```bash
uv run <this skill dir>/scripts/to_drive.py "<workdir>"
```

- It uploads the mp4s from `<workdir>/clips` to the **Musubi clips** shared drive under `Clips/<video title> clips` (characters Windows or Drive dislike are removed), makes the folder **Anyone with the link, Viewer** with `rclone link` (never edit), opens the link signed out to check it, and reads the channel from `source-audio.info.json`.
- If the user names the creator or brand, pass it as a second argument: `... to_drive.py "<workdir>" "Ved Iyer"` makes `Ved Iyer clips`.
- It prints JSON: `folder`, `uploaded`, `opens_signed_out`, `channel`, `youtube`, `drive`.
- Running it again after a re render replaces changed clips and keeps the same link. The review page and `clips.json` stay local.

When it fails:

- `rclone is not installed`: Mac `brew install rclone`, Windows `winget install Rclone.Rclone` (then open a new terminal). Ask the user first.
- `didn't find section in config file` (no `mktg` remote): ask the user to run `! rclone config create mktg drive scope=drive` and sign in with a musubiclip.com account that is a member of the **Musubi clips** shared drive.
- Token expired or `invalid_grant`: ask the user to run `! rclone config reconnect mktg:`.
- Shared drive not found: run `rclone backend drives mktg:`; the account is not a member of **Musubi clips**, so ask the user to get added.
- `opens_signed_out` is `false`: link sharing is blocked by an admin setting (Sharing outside musubiclip.com and Anyone with the link must be ON). Tell the user.

## 3. Report

Do everything in `musubi-clips` step 8 (open the review page, list each clip) and give the reminders below. Then **end the reply with exactly this block**, filled from the script's JSON, so it can be copied as is:

```
Channel: <channel>
YouTube: <youtube>
Drive: <drive>
```

Reminders:

- Watch each clip with sound before sending.
- Anyone who has the link can view and **download**, including whoever it is forwarded to (a Business Starter limit). To revoke, open the folder in Drive, Share, General access, Restricted.
- Share it privately with the creator or brand, never post it publicly.
