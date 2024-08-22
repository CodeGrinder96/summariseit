CHUNK_SUMMARY_PROMPT = """\
    Task: Extract the key takeways from podcast transcripts. Each transcript may be long, so it will be provided in chunks.

    Instructions: Summarise the provide chunk of text, focusing on the main points, key takeways, and lessons. \
        If a chunk of text is not informative or lacks substantive content, you can skip summarising it. Be concise.

    Context: {context}
""" 

FULL_SUMMARY_PROMPT = """\
    Task: Extract the key takeways from podcast transcripts. The transcript is dived into chunks, and a summary of each chunk is provided.
    
    Instructions: Based on the provided summaries of each chunk, write a short description of the podcast, and list the keytakeways in a concise, structured format. \
        Combine duplicate points or omit parts that are uninformative. Return everything in {output_language}. Be concise.
        
    Context: {context}
"""