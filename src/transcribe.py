from faster_whisper import WhisperModel

model = WhisperModel("base")

segments, info = model.transcribe("audio.mp3")

with open("transcript.txt", "w", encoding="utf-8") as f:
    for segment in segments:
        f.write(segment.text + "\n")

print("done")
