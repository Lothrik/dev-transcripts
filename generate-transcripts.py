from datetime import timedelta
from pathlib import Path
import whisper
import sys
import subprocess
import torch

target_folder = Path(__file__).parent / "transcripts"

model = whisper.load_model("large", device="cuda")
print("Whisper model loaded.")

def transcribe_audio(path):
    transcribe = model.transcribe(audio=str(path), language="en")
    segments = transcribe["segments"]

    output = ""
    for segment in segments:
        startTime = "0" + str(timedelta(seconds=int(segment["start"]))) + ",000"
        endTime = "0" + str(timedelta(seconds=int(segment["end"]))) + ",000"
        text = segment["text"]
        segmentId = segment["id"] + 1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        output = output + segment

    return output

def ffmpeg_installed():
    try:
        # Try to run "ffmpeg -version" to check if it's available
        result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
            return False
    
def cuda_installed():
    if torch.cuda.is_available():
        return True
    else:
        return False

if __name__ == "__main__":
    source_string = sys.argv[1] if len(sys.argv) > 1 else ''

    if not source_string:
        print("Error: Missing required parameter. Please provide a valid mp4 file or folder with mp4 files in it.")
        sys.exit(0)

    if not ffmpeg_installed():
        print("ffmpeg not installed or not on path paramater. Make sure ffmpeg is installed and added on to your path.")
        sys.exit(0)

    if not cuda_installed():
        print("cuda not installed or not on path paramater. Make sure cuda is installed and added on to your path.")
        sys.exit(0)

    source = Path(source_string)
    if source.is_file():
        file_list = [source]
    elif source.is_dir():
        file_list = source
    else:
        raise FileNotFoundError(f"The path '{source}' does not exist.")
    
    target_folder = Path(__file__).parent / "transcripts"
    if not Path.exists(target_folder):
        Path.mkdir(target_folder)

    for source_file in file_list:
        source_file_str = str(source_file)
        if source_file_str.lower().endswith('mp4'):
            target_path = source_file_str.replace(".mp4", ".srt")
            transcript = transcribe_audio(source_file)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            print("Finished processing: " + source_file_str)
        else:
            print("Skipping file since it's not a video: " + source_file_str)