from datetime import timedelta
from pathlib import Path
import whisper

target_folder = Path(__file__).parent / "transcripts"
source_files = []

model = whisper.load_model("base", device="cuda")
print("Whisper model loaded.")

def transcribe_audio(path):
    transcribe = model.transcribe(audio=path, language="en")
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

for source_file in source_files:
    source_path = (target_folder / source_file).as_posix()
    target_path = (target_folder / source_file.replace(".mp4", ".srt")).as_posix()
    transcript = transcribe_audio(source_path)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    print("Finished processing: " + source_file)