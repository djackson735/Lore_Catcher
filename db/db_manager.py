import sqlite3
import db.default_prompts as default_prompts


class DatabaseManager:

    def __init__(self, db_name='db/lore_catcher.db'):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        conn = sqlite3.connect('db/lore_catcher.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                summary TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                prompt TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                transcript TEXT
            )
        ''')

        # Insert default prompts
        for name, prompt in default_prompts.prompts:
            cursor.execute('INSERT INTO prompts (name, prompt) VALUES (?, ?)', (name, prompt))

        conn.commit()
        conn.close()

    def get_db_connection(self):
        return sqlite3.connect(self.db_name)

    def insert_prompt(self, name, prompt):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prompts (name, prompt) VALUES (?, ?)', (name, prompt))
        conn.commit()
        conn.close()

    def insert_transcript(self, transcript):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO transcripts (transcript) VALUES (?)', (transcript,))
        conn.commit()
        conn.close()

    def insert_formatted_summary(self, formatted_summary):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO summaries (summary) VALUES (?)', (formatted_summary,))
        conn.commit()
        conn.close()

    def get_recent_transcripts(self, limit=5):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT transcript FROM transcripts ORDER BY timestamp DESC LIMIT ?', (limit,))
        transcripts = cursor.fetchall()
        conn.close()
        return [transcript[0] for transcript in transcripts]

    def get_recent_summaries(self, limit=5):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT summary FROM summaries ORDER BY timestamp DESC LIMIT ?', (limit,))
        summaries = cursor.fetchall()
        conn.close()
        return [summary[0] for summary in summaries]

    def get_prompt(self, name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT prompt FROM prompts WHERE name = ?', (name,))
        prompt = cursor.fetchone()
        conn.close()
        return prompt[0] if prompt else None
