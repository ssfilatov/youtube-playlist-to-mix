from pydub import AudioSegment
import os
import argparse
import yt_dlp as youtube_dl

def download_and_convert(playlist_url):
    # Download the video using youtube-dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(".", '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except youtube_dl.DownloadError as e:
        print(f"Error downloading the playlist: {e}")


def mix_tracks(output_file):
    # List all the MP3 files in the input directory
    mp3_files = [f for f in os.listdir(".") if f.endswith(".mp3")]

    # Sort the files to ensure proper ordering
    mp3_files.sort()

    if len(mp3_files) == 0:
        return

    # Initialize the mixed audio
    mixed_audio = AudioSegment.from_file(os.path.join(".", mp3_files[0]), format="mp3")

    for mp3_file in mp3_files[1:]:
        # Load the next track
        next_track = AudioSegment.from_file(os.path.join(".", mp3_file), format="mp3")

	# Set the crossfade duration (in milliseconds)
        cross_fade_duration = 40000  # 40 seconds

        mixed_audio = mixed_audio.append(next_track, crossfade=cross_fade_duration)

    # Save the mixed audio to the output file
    mixed_audio.export(output_file, format="mp3")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mix MP3 tracks with high-pass and low-pass filters.")
    parser.add_argument("-i", "--input", help="Youtube playlist URL", required=True)
    parser.add_argument("-o", "--output", help="Output file for the mixed track", required=True)
    args = parser.parse_args()

    download_and_convert(args.input)
    # Mix the downloaded tracks
    mix_tracks(args.output)

