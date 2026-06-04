import yt_dlp

ydl_opts = {
    'format': 'best[ext=mp4]/best',
    'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'extractor_args': {
        'youtube': {
            'player_client': ['android']
        }
    }
}

url_input = input("Enter URLs: ")

urls = [u.strip() for u in url_input.split(',') if u.strip()]

for i, url in enumerate(urls):
    try:
        print(f"Downloading video {i + 1} from {url}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download {i + 1} completed.")
    except Exception as e:
        print(f"Error on video {i + 1}: {e}")

print("All downloads completed.")

