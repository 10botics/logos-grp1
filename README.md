# Rhythm Game

A Python-based rhythm game that combines music and video playback with interactive gameplay. Players must click circular buttons in time with the music as they light up randomly during video playback.

## Features

- Video background with synchronized audio playback
- Interactive circular buttons that light up during gameplay
- Score tracking system
- Hover effects in song selection menu
- Support for multiple songs
- Automatic video resizing to match source resolution
- Seamless loop playback for both video and audio

## Gameplay

- **Song Selection**: Choose from available songs in the menu
- **Controls**: 
  - Click the circular buttons when they light up yellow
  - Score 100 points for each successful hit
  - Press 'Q' at any time to quit
  - Press 'R' at game over to restart
- **Layout**:
  - Six circular buttons arranged in arrow formations on both sides
  - Score display in top-left corner
  - Tick counter in top-right corner
  - Video playback in the background

## Technical Details

- Built with Python using Pygame and OpenCV
- Supports MP4 video files with WAV audio
- Video playback synchronized with audio at native FPS
- Adaptive window sizing based on video resolution
- WAV audio configured for optimal playback (44.1kHz, 16-bit, stereo)

## Installation

1. Clone the repository

```bash
git clone <your-repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

To run the project:
```bash
python game.py
```

## Adding Songs

To add new songs to the game:

1. Place your song files in the `songs/` directory:
   ```
   songs/
   ├── song1.mp4    # Video file
   ├── song1.wav    # Audio file
   ├── song2.mp4
   ├── song2.wav
   └── ...
   ```

2. Edit the `songs` list in `game.py`:
   ```python
   self.songs = [
       {"title": "APT - ROSÉ & Bruno Mars", "video": "songs/song1.mp4", "audio": "songs/song1.wav", "pattern": []},
       {"title": "Your New Song", "video": "songs/your_video.mp4", "audio": "songs/your_audio.wav", "pattern": []},
       // Add more songs here
   ]
   ```

Requirements for song files:
- Video files should be in MP4 format
- Audio files should be in WAV format
- Both files should have the same duration
- File names should match their entry in the songs list

## Converting MP4 to WAV (Raspberry Pi)

1. Install FFmpeg if you haven't already:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

2. Navigate to your songs directory:
   ```bash
   cd songs
   ```

3. Convert MP4 to WAV:
   ```bash
   # For a single file
   ffmpeg -i song1.mp4 song1.wav

   # For multiple files at once
   for file in *.mp4; do
       ffmpeg -i "$file" "${file%.mp4}.wav"
   done
   ```

Note: The second command will convert all MP4 files in the current directory to WAV format.
If you get an error about audio codec, try adding `-acodec pcm_s16le`:
```bash
ffmpeg -i song1.mp4 -acodec pcm_s16le song1.wav
```

## License

[Choose an appropriate license]
