from datetime import timedelta
from pathlib import Path
import glob
import sys
import subprocess
import torch
import whisper

# turbo is the recommended model size, use medium or small if you encounter issues
model_size = "turbo" # https://github.com/openai/whisper#available-models-and-languages
audio_lang = "en"

# ".mp4" ".mkv" ".mov" ".webm" ".mp3" ".wav" ".m4a" -- anything ffmpeg can decode will work
source_ext = ".mp4"

# this is where the script will look for `source_ext` files, and where it will save transcripts
target_folder = Path(__file__).parent / "transcripts"

def ffmpeg_installed():
    try:
        # try to run "ffmpeg -version" to check if it's available
        result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
            return False

def transcribe_audio(path, audio_lang):
    transcribe = model.transcribe(audio=path, language=audio_lang)
    segments = transcribe["segments"]

    output = ""
    for segment in segments:
        startTime = f'0{str(timedelta(seconds=int(segment["start"])))},000'
        endTime = f'0{str(timedelta(seconds=int(segment["end"])))},000'
        text = segment["text"]
        segmentId = segment["id"] + 1
        if len(text) == 0:
            print(f"WARN: `transcribe_audio` returned zero-length text at segment {segmentId}.")
            text = " "
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        output = output + segment

    return output

if __name__ == "__main__":
    print(f'PyTorch version: {torch.__version__}')
    print(f'CUDA version: {torch.version.cuda}')
    print(f'Device name: {torch.cuda.get_device_properties("cuda").name}')
    print(f'FlashAttention available: {torch.backends.cuda.flash_sdp_enabled()}')

    if not ffmpeg_installed():
        print("ERROR: ffmpeg not installed or otherwise unavailable. Please verify installation and check PATH parameter.")
        sys.exit(0)

    torch_device = "cuda"
    if not torch.cuda.is_available():
        torch_device = "cpu"
        print("WARN: CUDA not installed or otherwise unavailable. Generating transcripts will be much slower than normal.")

    if not target_folder.is_dir():
        print(f'ERROR: `{target_folder}` does not point to a valid directory.')
        sys.exit(0)

    source_files = glob.glob(f"*{source_ext}", root_dir=target_folder)

    model = whisper.load_model(model_size, device=torch_device)
    print("Whisper model loaded.")

    print(f"Target folder: `{target_folder}` contains {len(source_files)} `{source_ext}` files, processing...")
    for source_file in source_files:
        source_path = (target_folder / source_file).as_posix()
        target_path = (target_folder / source_file.replace(source_ext, ".srt")).as_posix()
        if Path(target_path).is_file():
            print(f"Skipped processing: {source_file}")
        else:
            print(f"Started processing: {source_file}")
            transcript = transcribe_audio(source_path, audio_lang)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Finished processing: {source_file}")