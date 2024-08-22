import re

import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._transcripts import TranscriptListFetcher

from utils.whisper_utils import whisper_transcript


class YoutubeVideo:
    def __init__(self, url: str):
        self.url = url
        self.is_valid = self._validate_url()
        if self.is_valid:
            self.id = self._get_video_id()
    
    
    def _validate_url(self) -> bool:
        # Youtube oEmbed endpoint returns 200 for non-existent videos
        # We can check the json response to verify the video exists
        oembed_endpoint = f"https://www.youtube.com/oembed?url={self.url}&format=json"
        
        try:
            response = requests.get(oembed_endpoint)
            
            # If the response contains valid JSON, the video exists
            if response.status_code == 200:
                response_json = response.json()
                return 'title' in response_json
            else:
                return False
        except requests.exceptions.RequestException:
            return False
        except ValueError:
            return False


    def _get_video_id(self):
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',               # Standard and embedded URLs
            r'(?:youtu\.be\/|\/embed\/)([0-9A-Za-z_-]{11})'  # Short and embedded URLs
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.url)
            if match:
                return match.group(1)
        return None
    
    
    def get_default_caption_language_code(self) -> str:
        with requests.Session() as http_client:
            tListFetcher = TranscriptListFetcher(http_client)
            captions_json = tListFetcher._extract_captions_json(tListFetcher._fetch_video_html(self.id), self.id)
            defaultCaptionIndex = captions_json['audioTracks'][0].get('defaultCaptionTrackIndex', 0)
        
        get_default_caption_language_code = captions_json['captionTracks'][defaultCaptionIndex].get('languageCode')
        return get_default_caption_language_code


    def get_transcript(self) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.id)
            default_caption_language_code = self.get_default_caption_language_code()
            transcript_object = transcript_list.find_transcript([default_caption_language_code]) 
            if transcript_object.is_generated:
                transcript = whisper_transcript(self.url)
            else:
                transcript_raw = transcript_object.fetch()
                transcript = " ".join([entry['text'] for entry in transcript_raw])
        except Exception:
            transcript = whisper_transcript(self.url)
        return transcript

    
        
        