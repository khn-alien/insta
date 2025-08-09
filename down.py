import instaloader
import os
import shutil
from datetime import datetime, timedelta, timezone
import getpass

def main():
    # User inputs
    HASHTAG = input("🔍 Enter hashtag (without #): ").strip()
    try:
        LIMIT = int(input("📥 Enter number of videos to download: "))
    except ValueError:
        print("⚠️ Invalid number. Using default of 5.")
        LIMIT = 5

    try:
        DAYS = int(input("📅 Enter max age of posts in days (e.g., 7): "))
    except ValueError:
        print("⚠️ Invalid number. Using default of 7 days.")
        DAYS = 7

    USERNAME = input("👤 Enter Instagram username: ").strip()
    PASSWORD = getpass.getpass("🔑 Enter Instagram password: ")

    # Setup download folder
    DOWNLOAD_FOLDER = os.path.expanduser('~/storage/downloads/instagram_videos')
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    print(f"\n📁 Saving videos to: {DOWNLOAD_FOLDER}\n")

    # Setup Instaloader instance
    L = instaloader.Instaloader(
        save_metadata=False,
        post_metadata_txt_pattern='',
        download_pictures=False,
        download_video_thumbnails=False,
        compress_json=False
    )

    # Try to load session
    try:
        L.load_session_from_file(USERNAME)
        print("🔓 Logged in using saved session.")
    except:
        print("🔐 No saved session. Logging in manually...")
        try:
            L.login(USERNAME, PASSWORD)
            L.save_session_to_file()
            print("✅ Login successful. Session saved.")
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return

    # Get hashtag data
    try:
        hashtag = instaloader.Hashtag.from_name(L.context, HASHTAG)
    except Exception as e:
        print(f"❌ Failed to retrieve hashtag #{HASHTAG}: {e}")
        return

    count = 0
    now = datetime.now(timezone.utc)
    time_threshold = now - timedelta(days=DAYS)

    for post in hashtag.get_posts():
        if post.is_video and post.date_utc >= time_threshold:
            video_filename = f"{post.shortcode}.mp4"
            final_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

            if os.path.exists(final_path):
                print(f"⚠️ Skipping duplicate: {video_filename}")
                continue

            temp_folder = "_temp_download"
            os.makedirs(temp_folder, exist_ok=True)

            print(f"⬇️ Downloading video: {post.shortcode} | Date: {post.date_utc.strftime('%Y-%m-%d')}")

            try:
                L.download_post(post, target=temp_folder)

                # Move video file to target folder
                moved = False
                for file in os.listdir(temp_folder):
                    if file.endswith(".mp4"):
                        shutil.move(os.path.join(temp_folder, file), final_path)
                        moved = True
                        break

                if not moved:
                    print(f"⚠️ Warning: No video file found for post {post.shortcode}")

            except Exception as e:
                print(f"❌ Failed to download {post.shortcode}: {e}")

            # Clean up temp folder
            shutil.rmtree(temp_folder, ignore_errors=True)

            count += 1
            print(f"✅ Downloaded {count}/{LIMIT} videos.\n")

            if count >= LIMIT:
                break

    print(f"🎉 Done! {count} videos saved in '{DOWNLOAD_FOLDER}'.")

if __name__ == "__main__":
    main()
