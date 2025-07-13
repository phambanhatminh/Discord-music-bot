# 🎶 Kaoruko - A Discord Music Bot

Kaoruko is a feature-rich Discord music bot built with `discord.py` and `yt-dlp`. It supports YouTube song search, queue management, and auto-disconnects after inactivity.

## Features

- 🔍 Search and play songs by name or link
- 📜 Song queue with titles (not just URLs)
- ⏸️ Pause, resume, skip, and stop playback
- ➕ Automatically joins your voice channel
- ⏱️ Auto-disconnects after 3 minutes of inactivity
- 🔊 Volume control (via FFmpeg options)

## Commands

| Command         | Description                                  |
|----------------|----------------------------------------------|
| `?play <song>` | Plays a song or adds it to the queue         |
| `?queue`       | Shows the current queue                      |
| `?skip`        | Skips to the next song in queue              |
| `?pause`       | Pauses the current song                      |
| `?resume`      | Resumes a paused song                        |
| `?stop`        | Stops music and disconnects from voice chat  |
| `?clear_queue` | Clears the song queue                        |

## Installation

1. **Clone this repo**
   ```bash
   git clone https://github.com/yourusername/discord-music-bot.git
   cd discord-music-bot

   2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file**
   ```env
   discord_token=YOUR_DISCORD_BOT_TOKEN
   ```

4. **Run the bot**
   ```bash
   python main.py
   ```

## Requirements

- Python 3.9+
- [FFmpeg](https://ffmpeg.org/download.html) (must be in your system PATH)
- `discord.py`
- `yt-dlp`
- `python-dotenv`

You can install everything via:

```bash
pip install -r requirements.txt
```

Sample `requirements.txt`:
```
discord.py
yt-dlp
python-dotenv
```

## Notes

- The bot joins the same voice channel as the command sender.
- Songs are played using YouTube audio streams.
- It auto-disconnects after 3 minutes if the queue is empty.

## License

MIT License

---

Made by **Minh Pham**
