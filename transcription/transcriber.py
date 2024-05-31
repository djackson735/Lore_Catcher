import datetime


class Transcriber:
    def __init__(self, file_queue, transcript_queue, client):
        self.file_queue = file_queue
        self.transcript_queue = transcript_queue
        self.client = client

    async def transcribe_audio(self):
        while True:
            file_name = await self.file_queue.get()
            print(f"{datetime.datetime.now()} - Transcribing audio started on file {file_name}")

            try:
                audio_file = open(file_name, "rb")
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                print(f"Transcript: {transcript}")
                await self.transcript_queue.put(transcript)

            except Exception as e:
                print(f"Error transcribing file {file_name}: {e}")

            finally:
                self.file_queue.task_done()
