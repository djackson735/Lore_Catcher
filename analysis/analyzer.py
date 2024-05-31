import datetime


class Analyzer:
    def __init__(self, transcript_queue, client):
        self.transcript_queue = transcript_queue
        self.client = client

    async def summarize_transcript(self):
        """
        Summarizes transcripts from the transcript_queue using OpenAI's GPT-3.5-turbo model.
        """
        while True:
            transcript = await self.transcript_queue.get()
            print(f"{datetime.datetime.now()} - Summarizing transcript started")

            try:
                completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                    "Your task is to summarize a section of a transcript that is being passed to you. The " +
                                    "challenge is that the section you're given is part of a larger transcript, and may " +
                                    "start or end in the middle of a sentence. Summarize it succinctly, using context clues " +
                                    "to understand the beginning and where it's going."
                            )
                        },
                        {
                            "role": "user",
                            "content": transcript
                        }
                    ]
                )
                summary = completion.choices[0].message.content
                print(f"Summary: {summary}")
            except Exception as e:
                print(f"Error summarizing transcript: {e}")

            self.transcript_queue.task_done()