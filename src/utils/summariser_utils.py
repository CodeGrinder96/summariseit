
import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from prompts.prompts import *

load_dotenv()


chat_model = AzureChatOpenAI(
    deployment_name='gpt-4o',
    openai_api_key=os.getenv('OPENAI_API_KEY'),
    azure_endpoint=os.getenv('OPENAI_ENDPOINT'),
    openai_api_version=os.getenv('OPENAI_API_VERSION'),    
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000,
    chunk_overlap=25,
)


async def summarize_chunk(chunk):
    _summary = await chat_model.ainvoke(CHUNK_SUMMARY_PROMPT.format(context=chunk))
    return _summary.content

async def get_summary_async(transcript: str, output_language: str):
    chunks = text_splitter.split_text(transcript)
    print(f'Number of chunks {len(chunks)}')
    
    history = await asyncio.gather(*[summarize_chunk(chunk) for chunk in chunks])
    full_summary = chat_model.invoke(FULL_SUMMARY_PROMPT.format(context=history, output_language=output_language)).content
    return full_summary