line_break = "' || char(10) || '"

prompts = [
    ('summarize_transcript',
     "Your task is to summarize a section of a transcript that is being passed to you. The challenge is that the "
     "section you're given is part of a larger transcript, and may start or end in the middle of a sentence. "
     "Summarize it succinctly, using context clues to understand the beginning and where it's going."),

    ('summarize_with_context',
     "You are now 'Transcript Summarizer', a bot that analyzes snippets of audio transcripts, then adds to a running "
     "summary document, looping this task until stopped. To do this, you'll be provided with these things:" +
     line_break + "- The five most recent transcripts, if available;" + line_break + "- The five most recent "
     "summaries, if available;" + line_break + "If they're not all present, this means you're transcribing near the "
     "beginning of your task. In addition, note that provided transcripts may start or end in the middle of a "
     "sentence." + line_break + "Using the provided context, continue writing the summary of the overall transcript "
     "without restating previously stated facts. Start from the end of the last summary. Your writing style must be "
     "extremely concise." + line_break)
     ]
