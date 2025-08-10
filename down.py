import os
import subprocess

def get_download_path():
    path = os.path.join(os.environ["HOME"], "storage", "downloads", "shorts_videos")
    os.makedirs(path, exist_ok=True)
    return path

def main():
    print("📺 YouTube Shorts/Video Downloader by Keyword (No Login Required)\n")

    keyword = input("🔍 Enter keyword or genre to search: ").strip()
    count = input("🎯 How many videos to download? (default 5): ").strip()

    try:
        count = int(count)
    except:
        count = 5

    output_dir = get_download_path()
    print(f"\n⬇️ Downloading top {count} videos for keyword: '{keyword}' ...\n")

    cmd = [
        "yt-dlp",
        f"ytsearch{count}:{keyword} shorts",
        "-f", "mp4",
        "-o", f"{output_dir}/%(title).50s.%(ext)s",
        "--no-playlist"
    ]

    subprocess.run(cmd)

    print(f"\n✅ Download complete! Videos saved in:\n📁 {output_dir}")

if __name__ == "__main__":
    main()
