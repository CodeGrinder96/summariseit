
import asyncio
from threading import Lock
from typing import Optional

from dotenv import load_dotenv

# from langchain_openai import AzureChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models.llm_factory import LLMFactory
from prompts.prompts import *
from pydantic import BaseModel, Field

load_dotenv()

class SummaryModel(BaseModel):
    response: str = Field(description="Your summary of the podcast")
    
    
class Summariser():
    _llm: Optional[LLMFactory] = None
    _text_splitter: Optional[RecursiveCharacterTextSplitter] = None
    _lock = Lock()
    
    def __init__(self):
        with Summariser._lock:
            if Summariser._llm is None:    
                Summariser._llm = LLMFactory('azure_openai')
            if Summariser._text_splitter is None:
                Summariser._text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=5000,
                    chunk_overlap=25,
                )
        self.llm = Summariser._llm
        self.text_splitter = Summariser._text_splitter


    async def _summarize_chunk(self, chunk: str) -> Optional[str]:
        try:
            summary = await self.llm.create_completion(
                response_model=SummaryModel,
                messages = [
                    {
                        "role": "system", 
                        "content": CHUNK_SUMMARY_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": chunk,
                    },
                ]
            )
            return summary.response
        except Exception as e:
            print(f"Error summarising chunk: {e}")
            return None


    async def get_summary_async(self, transcript: str, output_language: str) -> Optional[str]:
        chunks = self.text_splitter.split_text(transcript)    
        history = await asyncio.gather(*[self._summarize_chunk(chunk) for chunk in chunks])
        try: 
            full_summary = await self.llm.create_completion(
                response_model=SummaryModel,
                messages = [
                    {
                        "role": "system", 
                        "content": FULL_SUMMARY_PROMPT.format(output_language=output_language),
                    },
                    {
                        "role": "user",
                        "content": f"{history}",
                    },
                ]
            )
            return full_summary.response
        except Exception as e:
            print(f"Error summarising the podcast: {e}")
            return None






