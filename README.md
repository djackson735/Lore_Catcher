# Lore Catcher
Lore Catcher is a tool designed to assist Dungeon Masters during Dungeons & Dragons sessions by automating the note-taking process. It listens to the Dungeon Master in real-time and generates short summaries of the game's progress every three minutes.

The project leverages the Whisper API for audio processing and GPT-3.5 Turbo to analyze the Dungeon Master's audio and summarize the events. Rather than using speech-to-text solutions, Whisper is used for its automatic formatting and punctuation, which aids the analyzer in determining what's going on. Summaries are stored in a SQLite3 database.

## Current Features
- Real-time Summaries: Automatically generates summaries of gameplay every three minutes.
- Contextual Understanding: Uses previously created summaries to add context in a natural way.
- Audio Analysis: Utilizes the Whisper API for audio clarity and GPT-3.5 Turbo for summarization.

## Planned Features
- Master Campaign Note: A continuous document of D&D session notes built from real-time summaries.
- Custom "About My Party" prompt creation, to inform the model about the characters in the party.
- Semantic search of the database to better inform on key events, characters, or other details.

## Installation
This project is currently in development and not ready for installation. However, you can set up the development environment with the following steps:

Clone the repository:

Copy code
```
git clone https://github.com/djackson735/Lore_Catcher.git
```
Navigate to the project directory:
```
cd your-repo
```
Install the required Python packages:
```
pip install -r requirements.txt
```

**Reporting Issues**
If you encounter any bugs or issues, please report them in the Issues section of the repository.

## License
This project is licensed under a non-commercial use license. See the LICENSE file for details.

## Acknowledgements

This application uses the following APIs:

- [OpenAI GPT-3.5](https://openai.com/api/)
- [OpenAI Whisper](https://openai.com/index/whisper/)

These APIs are provided by OpenAI and used in compliance with their [Terms of Service](https://openai.com/policies/terms-of-use/).

## Security

If you clone this repository and submit a pull request, ensure you *do not make your OpenAI API key public*. Add your .env file to your gitignore if you choose to include it locally. Always use the software in an ethical and responsible manner.
