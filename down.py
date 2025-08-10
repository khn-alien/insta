import os
import subprocess

def get_download_path():
    path = os.path.join(os.environ["HOME"], "storage", "downloads", "shorts_videos")
    os.makedirs(path, exist_ok=True)
    return path

def main():
    print("📺 YouTube Shorts Downloader (High Quality, ≤30 sec)\n")

    keyword = input("🔍 Enter keyword or genre to search: ").strip()
    count = input("🎯 How many videos to download? (default 5): ").strip()

    try:
        count = int(count)
    except:
        count = 5

    output_dir = get_download_path()
    print(f"\n⬇️ Downloading top {count} videos for keyword: '{keyword}' with max 30 sec length...\n")

    cmd = [
        "yt-dlp",
        f"ytsearch{count}:{keyword} shorts",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "--match-filter", "duration <= 30",
        "-o", f"{output_dir}/%(title).50s.%(ext)s",
        "--no-playlist",
        "--merge-output-format", "mp4"
    ]

    subprocess.run(cmd)

    print(f"\n✅ Download complete! Videos saved in:\n📁 {output_dir}")

if __name__ == "__main__":
    main()
