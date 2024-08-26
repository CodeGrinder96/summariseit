import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import whisper
from pytubefix import YouTube
from pytubefix.cli import on_progress


class WhisperWrapper():
    _model = None
    _loading = False
    _lock = Lock()
    
    def __init__(self, url: str):
        with WhisperWrapper._lock:
            if WhisperWrapper._model is None and not WhisperWrapper._loading:
                WhisperWrapper._loading = True
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(self._load_model)
                    WhisperWrapper._model = future.result()
                WhisperWrapper._loading = False
        self.model = WhisperWrapper._model   
        self.url = url
        self._data_dir = os.path.join(os.getcwd(), 'src', 'data')
        self._filepath = os.path.join(self._data_dir, 'tmp.mp3')

    @classmethod
    def _load_model(cls):
        try:
            return whisper.load_model('tiny')
        except Exception as e:
            print(f'Error loading Whisper model: {e}')
            raise
    
    def _download_audio(self) -> None:
        try:
            youtube = YouTube(self.url, on_progress_callback=on_progress)
            youtube_stream = youtube.streams.get_audio_only()
            youtube_stream.download(output_path=self._data_dir, filename='tmp', mp3=True)
        except Exception as e:
            print(f"Error downloading audio: {e}")
            raise

    def _delete_audio(self) -> None:
        try: 
            os.remove(self._filepath)
        except Exception as e:
            print(f"Error deleting audio file: {e}")
            raise    
    
    def get_transcript(self) -> str:
        self._download_audio()
        try:
            transcript = self.model.transcribe(self._filepath)['text']
        finally:
            self._delete_audio()
        return transcript