import instaloader
import os
import shutil
from datetime import datetime, timedelta

def main():
    # Inputs from user
    HASHTAG = input("Enter hashtag (without #): ").strip()
    try:
        LIMIT = int(input("Enter number of videos to download: "))
    except ValueError:
        print("Invalid number. Using default of 5.")
        LIMIT = 5

    try:
        DAYS = int(input("Enter max age of posts in days (e.g., 7 for last week): "))
    except ValueError:
        print("Invalid number. Using default of 7 days.")
        DAYS = 7

    # Setup download folder in Termux storage downloads
    DOWNLOAD_FOLDER = os.path.expanduser('~/storage/downloads/instagram_videos')
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    print(f"Saving videos to: {DOWNLOAD_FOLDER}")

    L = instaloader.Instaloader()

    # Uncomment to login (optional, helps if you want more results or private content)
    # L.login('your_username', 'your_password')

    hashtag = instaloader.Hashtag.from_name(L.context, HASHTAG)

    count = 0
    now = datetime.now()
    time_threshold = now - timedelta(days=DAYS)

    for post in hashtag.get_posts():
        if post.is_video and post.date_utc >= time_threshold:
            video_filename = f"{post.shortcode}.mp4"
            final_path = os.path.join(DOWNLOAD_FOLDER, video_filename)

            if os.path.exists(final_path):
                print(f"Skipping duplicate: {video_filename}")
                continue

            temp_folder = "_temp_download"
            os.makedirs(temp_folder, exist_ok=True)

            print(f"Downloading video: {post.shortcode} from #{HASHTAG}")
            L.download_post(post, target=temp_folder)

            # Move .mp4 file to final folder
            moved = False
            for file in os.listdir(temp_folder):
                if file.endswith(".mp4"):
                    shutil.move(os.path.join(temp_folder, file), final_path)
                    moved = True
                    break

            if not moved:
                print(f"Warning: No video file found for post {post.shortcode}")

            # Clean temp folder
            shutil.rmtree(temp_folder, ignore_errors=True)

            count += 1
            print(f"Downloaded {count}/{LIMIT} videos.")

            if count >= LIMIT:
                break

    print(f"✅ Done! {count} videos saved in '{DOWNLOAD_FOLDER}'.")

if __name__ == "__main__":
    main()
