# dev-transcripts
 
Developer update and interview transcripts generated with https://github.com/openai/whisper and https://github.com/yt-dlp/yt-dlp.

# how to use

Step 1: install python (3.11 or later is recommended):  https://www.python.org/downloads/

Step 2: install ffmpeg (or add an existing installation to your PATH):  https://www.ffmpeg.org/download.html

Step 3: install CUDA:  https://developer.nvidia.com/cuda-downloads

Step 4: uninstall PyTorch:  `pip3 uninstall torch torchvision torchaudio`

Step 5: reinstall PyTorch:  https://pytorch.org/

Step 6: install OpenAI-Whisper:  `pip3 install -U openai-whisper`

Step 7: configure `model_size`, `audio_lang`, `source_ext`, and `target_folder` if required in `generate-transcripts.py`

Step 8: run `generate-transcripts.py` via python3