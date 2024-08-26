CHUNK_SUMMARY_PROMPT = """\
    Task: Summarize key takeaways from a podcast transcript. The transcript is provided in chunks.

    Instructions: Summarize the main points, key takeaways, and lessons from the provided chunk. Skip summarizing if the content lacks substance or relevance. 
    Be concise but ensure all critical aspects are covered. 
"""

FULL_SUMMARY_PROMPT = """\
    Task: Create a Markdown-formatted summary of a podcast based on chunk summaries.

    Instructions:
    1. Write a brief **Overview** of the podcast in a single paragraph.
    2. List the **Key Takeaways** using bullet points. Each key takeaway should be concise and start with a bolded keyword if possible.
    3. If applicable, provide a list of **Lessons** learned, also using bullet points.
    4. Ensure all sections are clearly separated with appropriate Markdown headings (e.g., `### Overview`, `### Key Takeaways`, `### Lessons`).
    5. Combine duplicate points, omit any irrelevant information, and ensure the summary is well-organized and concise.
    6. Focus on the main message of the podcast. Ignore side tracks such as advertisement, selling courses, call to action, etc.
    6. The entire summary should be returned in {output_language}.

    Example format:

    ### Overview
    Brief summary of the podcast.

    ### Key Takeaways
    - **Key Point 1**: Description of the key point.
    - **Key Point 2**: Description of the key point.

    ### Lessons
    - **Lesson 1**: Description of the lesson.
    - **Lesson 2**: Description of the lesson.
"""
