import os

import whisper
from pytubefix import YouTube
from pytubefix.cli import on_progress

model = whisper.load_model('tiny')
root = os.path.dirname(os.path.abspath(__file__ + '/../'))


def download_audio(url: str) -> None:
    youtube = YouTube(url, on_progress_callback=on_progress)
    
    youtube_stream = youtube.streams.get_audio_only()
    youtube_stream.download(output_path=os.path.join(root, 'data'), filename='tmp', mp3=True)
    

def delete_audio(filepath: str) -> None:
    os.remove(filepath)
    
def whisper_transcript(url: str) -> str:
    filepath = os.path.join(root, 'data', 'tmp.mp3')
    download_audio(url)
    transcript = model.transcribe(filepath)['text']
    delete_audio(filepath)
    return transcript