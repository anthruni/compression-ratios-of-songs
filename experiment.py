import yt_dlp
import os

#search for a song and download it as tmp_song.mp3
# use ytsearch to search for a song
def download_song(song_name):

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'tmp_song',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }
    
    song_name = "ytsearch:" + song_name

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([song_name])

song_name = input("Enter song name: ")
download_song(song_name)

uncompressed = os.popen("du -b tmp_song.wav").read().split()[0]

os.system("gzip tmp_song.wav")
compressed = os.popen("du -b tmp_song.wav.gz").read().split()[0]

print(f"ratio: {int(compressed)/int(uncompressed):.2f}")

os.system(f"mv tmp_song.wav.gz {song_name.replace(' ', '_')}.mp3.gz")


with open("lyrics_ratios_log", "a") as f:
    f.write(f"{int(compressed)/int(uncompressed):.2f}|{song_name}.wav\n")
