import yt_dlp

ydl_opts = {
    'format': 'best/bestvideo+bestaudio',
    'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s', 
}

url_input = input("Enter URLs:  ")

urls = [url.strip() for url in url_input.split(',') if url.strip()]

for i, url in enumerate(urls):
    try:
        print(f"Downloading video {i + 1} from {url}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download {i + 1} completed.")
    except Exception as e:
        print(f"An error occurred while downloading video {i + 1} from {url}: {e}")

print("All downloads (if any) are completed.")



