
import asyncio
from threading import Lock
from typing import List, Optional

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

    def _split_text_into_chunks(self, transcript: str) -> List[str]:
        return self.text_splitter.split_text(transcript)

    async def _summarize_chunks(self, chunks: List[str]) -> List[str]:
        return await asyncio.gather(*[self._summarize_chunk(chunk) for chunk in chunks])

    async def _create_full_summary(self, chunk_summaries: list[str], output_language: str):
        history = " ".join(chunk_summaries)
        full_summary = await self.llm.create_completion(
            response_model=SummaryModel,
            messages=[
                {
                    "role": "system", 
                    "content": FULL_SUMMARY_PROMPT.format(output_language=output_language)
                },
                {
                    "role": "user", 
                    "content": history},
            ]
        )
        return full_summary.response
    
    async def get_summary_async(self, transcript: str, output_language: str):
        chunks = self._split_text_into_chunks(transcript)
        chunk_summaries = await self._summarize_chunks(chunks)
        full_summary = await self._create_full_summary(chunk_summaries, output_language)
        return full_summary