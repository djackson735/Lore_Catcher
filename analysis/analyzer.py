import datetime


class Analyzer:
    def __init__(self, transcript_queue, client, db_manager):
        self.transcript_queue = transcript_queue
        self.client = client
        self.db_manager = db_manager

    async def summarize_transcript(self, prompt_name="summarize_transcript"):
        """
        Summarizes transcripts from the transcript_queue using OpenAI's GPT-3.5-turbo model.
        """
        while True:
            transcript = await self.transcript_queue.get()
            print(f"{datetime.datetime.now()} - Summarizing transcript started")

            try:
                prompt = self.db_manager.get_prompt(prompt_name)
                completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": prompt
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

    async def summarize_with_context(self, prompt_name="summarize_with_context"):
        """
        More sophisticated summary function that uses get_recent_summaries to provide context to the model. Also
        fetches the last five transcriptions.
        """
        while True:
            transcript = await self.transcript_queue.get()
            print(f"{datetime.datetime.now()} - Summarizing transcript with context started")

            try:
                prompt = self.db_manager.get_prompt(prompt_name)
                recent_summaries = self.db_manager.get_recent_summaries()
                recent_transcripts = self.db_manager.get_recent_transcripts()
                completion = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": prompt
                        },
                        {
                            "role": "user",
                            "content": "- Recent Transcripts:" + "\n" + "\n".join(recent_transcripts) + "\n" +
                                       "- Recent Summaries:" + "\n" + "\n".join(recent_summaries) + "\n" +
                                       "- Current Transcript" + "\n" + transcript
                        }
                    ]
                )
                summary = completion.choices[0].message.content
                formatted_summary = "SUMMARY:" + chr(10) + summary
                print(formatted_summary)
                self.db_manager.insert_formatted_summary(formatted_summary)

            except Exception as e:
                print(f"Error summarizing transcript with context: {e}")

            finally:
                self.transcript_queue.task_done()





