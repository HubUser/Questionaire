This project provides a simple GUI application to present text questions to a user and record their spoken answers as audio files.

## Requirements

- Python 3
- Install dependencies with:

  ```bash
  pip install -r requirements.txt
  ```

- Additional system dependencies for audio and GUI support (especially on Linux or WSL):

  ```bash
  sudo apt-get install python3-tk
  sudo apt update
  sudo apt install -y libportaudio2 libasound2-plugins pulseaudio-utils alsa-utils ffmpeg
  ```

## Usage

1. Run the application via `main.py` with command line arguments specifying the questions file and output directory:

    ```bash
    python main.py --questions path/to/questions.txt --output_dir path/to/output_directory
    ```

2. The GUI window will display a question.
3. Click "Record Answer" to start recording your voice answer.
4. Click "Stop Recording" to stop and save the audio as an MP3 file in the specified output directory with filenames `answer_#.mp3`.
5. Click "Next Question" to proceed to the next question.
6. Repeat steps 3-5 for all questions.
7. When there are no more questions, the application will exit.

## How it Works

- The application uses the system microphone to record audio.
- Audio is first saved temporarily as WAV, then converted and saved as MP3.
- Recorded files are saved in the working directory with filenames corresponding to the question order.

## Notes

- Run the app where you have permissions to record audio and write files.
- Compatible with Windows (native or WSLg) and Linux with the necessary system libraries installed.
