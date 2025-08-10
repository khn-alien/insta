import os
import subprocess
from datetime import datetime, timedelta
import json
import sys

def get_download_path():
    path = os.path.join(os.environ["HOME"], "storage", "downloads", "shorts_videos")
    os.makedirs(path, exist_ok=True)
    return path

def run_command(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("❌ Command failed:", result.stderr)
        sys.exit(1)
    return result.stdout

def list_formats(url):
    # Get formats info for the first video in search results
    print("\n⏳ Fetching video info to show available formats...")
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--dump-json",
        url,
    ]
    output = run_command(cmd)
    info = json.loads(output)
    formats = info.get("formats", [])
    # Filter mp4 video formats with video and audio
    filtered = [f for f in formats if f.get("ext") == "mp4" and f.get("vcodec") != "none" and f.get("acodec") != "none"]
    print("\nAvailable mp4 video+audio formats:")
    for f in filtered:
        print(f"Format code: {f['format_id']}, Resolution: {f.get('resolution') or f.get('height')}p, FPS: {f.get('fps')}, filesize: {f.get('filesize') or 'unknown'} bytes")
    return filtered

def main():
    print("📺 YouTube Shorts Downloader - Interactive\n")

    keyword = input("🔍 Enter keyword or genre to search: ").strip()
    count_str = input("🎯 How many videos to download? (default 5): ").strip()
    max_length_str = input("⏱ Max video length in seconds (default 30): ").strip()
    max_age_str = input("📅 Max video age in days (0 for no limit, default 0): ").strip()

    count = int(count_str) if count_str.isdigit() else 5
    max_length = int(max_length_str) if max_length_str.isdigit() else 30
    max_age_days = int(max_age_str) if max_age_str.isdigit() else 0

    search_url = f"ytsearch{count}:{keyword} shorts"

    # Get first video info to list formats
    print(f"\n🔎 Searching videos for '{keyword}'...\n")
    cmd_info = [
        "yt-dlp",
        "--skip-download",
        "--dump-json",
        f"ytsearch1:{keyword} shorts"
    ]
    try:
        info_json = run_command(cmd_info)
        info = json.loads(info_json)
    except Exception as e:
        print(f"❌ Failed to fetch video info: {e}")
        sys.exit(1)

    # Show available formats for first video
    filtered_formats = list_formats(info['webpage_url'])

    # Choose format code
    format_code = input("\nEnter format code to download (or leave empty for best): ").strip()
    if not format_code:
        format_code = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"

    # Prepare filters
    filters = [f"duration <= {max_length}"]
    if max_age_days > 0:
        cutoff = datetime.now() - timedelta(days=max_age_days)
        cutoff_iso = cutoff.strftime("%Y%m%d")
        filters.append(f"upload_date > {cutoff_iso}")

    filter_expr = " and ".join(filters)

    print(f"\n⬇️ Downloading top {count} videos for keyword '{keyword}' with filters:")
    print(f" - Max length: {max_length} seconds")
    if max_age_days > 0:
        print(f" - Uploaded after: {cutoff.strftime('%Y-%m-%d')}")
    else:
        print(" - No upload date limit")

    output_dir = get_download_path()

    cmd_download = [
        "yt-dlp",
        search_url,
        "-f", format_code,
        "--match-filter", filter_expr,
        "-o", f"{output_dir}/%(title).50s.%(ext)s",
        "--no-playlist",
        "--merge-output-format", "mp4",
    ]

    subprocess.run(cmd_download)

    print(f"\n✅ Download complete! Check your videos in:\n📁 {output_dir}")

if __name__ == "__main__":
    main()
