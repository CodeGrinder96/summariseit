import os
from concurrent.futures import ThreadPoolExecutor

import whisper
from pytubefix import YouTube
from pytubefix.cli import on_progress


class WhisperWrapper():
    _model = None
    _loading = False
    
    def __init__(self, url: str):
        if WhisperWrapper._model is None and not WhisperWrapper._loading:
            WhisperWrapper._loading = True
            with ThreadPoolExecutor() as executor:
                future = executor.submit(self._load_model)
                WhisperWrapper._model = future.result()
            WhisperWrapper._loading = False
        self.model = WhisperWrapper._model   
        self.url = url
        self.data_dir = os.path.join(os.getcwd(), 'src', 'data')

    
    @classmethod
    def _load_model(self):
        print('Loading model')
        return whisper.load_model('tiny')
    
    
    def _download_audio(self) -> None:
        youtube = YouTube(self.url, on_progress_callback=on_progress)
        
        youtube_stream = youtube.streams.get_audio_only()
        youtube_stream.download(output_path=self.data_dir, filename='tmp', mp3=True)
    

    def _delete_audio(self) -> None:
        os.remove(self.filepath)
    
    
    def get_transcript(self) -> str:
        self.filepath = os.path.join(self.data_dir, 'tmp.mp3')
        self._download_audio()
        transcript = self.model.transcribe(self.filepath)['text']
        self._delete_audio()
        return transcript