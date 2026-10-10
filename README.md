# Unseen Files — daily video publishing

This repository provides a scheduled Facebook video publisher for the **Unseen Files** page.

## Important limitation: Google Flow generation

Google Flow does not provide a supported public API for automatically creating videos from GitHub Actions. This workflow therefore **does not generate a video or consume Flow credits**. Create a video in Flow first, then update the `VIDEO_URL` repository variable to a direct, publicly reachable MP4 URL for that day's video. Do not use a normal webpage/share page; Facebook needs to fetch the actual video file.

## Configure GitHub

In **Settings → Secrets and variables → Actions**, add:

### Repository secrets
- `FB_PAGE_ACCESS_TOKEN` — a valid Facebook Page access token with permission to publish videos to the Page. Keep it secret; never commit it to this repository.

### Repository variables
- `FB_PAGE_ID` — `1360132067172555` (Unseen Files page).
- `VIDEO_URL` — direct HTTPS URL to the MP4 for the next post.
- `VIDEO_DESCRIPTION` — optional caption. If empty, a default Unseen Files caption is used.

The video URL must point to a publicly accessible MP4 that Facebook can download. The workflow remembers the last posted URL in `state/last_video_url.txt` and skips a repeat URL. After a successful post, update `VIDEO_URL` to the next day's video.

## Schedule

The workflow is scheduled for **8:00 PM Sri Lanka time** (14:30 UTC). GitHub Actions schedules are best-effort and can start late. You can also run it manually from **Actions → Unseen Files Daily Publisher → Run workflow**.

## What it does

1. Checks that today's video URL and Facebook credentials are configured.
2. Skips if the same URL was already published.
3. Asks Facebook to publish the MP4 URL to the configured Page.
4. Saves the posted URL so a rerun does not publish the same video twice.

## Fully automatic Flow generation

To make the entire pipeline hands-off, an officially supported video-generation API or another permitted automation path for Flow is still needed. Browser automation of the Flow website is not included because login challenges and UI changes can make it unreliable. This setup intentionally does not claim to generate videos automatically.
