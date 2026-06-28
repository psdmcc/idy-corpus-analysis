import pandas as pd
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
import time

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

QUEUE_FILE = (
    "data/analysis/transcript_recovery_queue.csv"
)

OUTPUT_DIR = Path(
    "data/transcripts_recovered_pilot"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

METADATA_FILE = (
    OUTPUT_DIR /
    "pilot_metadata.csv"
)

PILOT_SIZE = 100

# --------------------------------------------------
# LOAD QUEUE
# --------------------------------------------------

queue = pd.read_csv(
    QUEUE_FILE
)

queue = queue.head(PILOT_SIZE)

ytt = YouTubeTranscriptApi()

results = []

# --------------------------------------------------
# TRANSCRIPT CHOICE
# --------------------------------------------------

def choose_transcript(transcript_list):

    transcripts = list(transcript_list)

    # manual english
    for t in transcripts:
        if (
            t.language_code.startswith("en")
            and not t.is_generated
        ):
            return t

    # auto english
    for t in transcripts:
        if (
            t.language_code.startswith("en")
            and t.is_generated
        ):
            return t

    # manual hindi
    for t in transcripts:
        if (
            t.language_code == "hi"
            and not t.is_generated
        ):
            return t

    # auto hindi
    for t in transcripts:
        if (
            t.language_code == "hi"
            and t.is_generated
        ):
            return t

    return transcripts[0]

# --------------------------------------------------
# HARVEST
# --------------------------------------------------

for i, video_id in enumerate(
    queue["video_id"].astype(str),
    start=1
):

    print(
        f"[{i}/{PILOT_SIZE}] {video_id}"
    )

    try:

        transcript_list = ytt.list(
            video_id
        )

        transcript = choose_transcript(
            transcript_list
        )

        data = transcript.fetch()

        text = "\n".join(
            row.text
            for row in data
        )

        outfile = (
            OUTPUT_DIR /
            f"{video_id}.{transcript.language_code}.txt"
        )

        with open(
            outfile,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(text)

        results.append({
            "video_id":
                video_id,

            "success":
                True,

            "language":
                transcript.language_code,

            "generated":
                transcript.is_generated,

            "segments":
                len(data),

            "words":
                len(text.split()),

            "characters":
                len(text),

            "outfile":
                str(outfile),

            "error":
                ""
        })

        print(
            "  SUCCESS",
            transcript.language_code,
            "| segments:",
            len(data),
            "| words:",
            len(text.split())
        )

    except Exception as e:

        results.append({
            "video_id":
                video_id,

            "success":
                False,

            "language":
                "",

            "generated":
                "",

            "segments":
                0,

            "words":
                0,

            "characters":
                0,

            "outfile":
                "",

            "error":
                str(e)
        })

        print(
            "  FAIL",
            type(e).__name__
        )

    time.sleep(1)

# --------------------------------------------------
# SAVE METADATA
# --------------------------------------------------

meta = pd.DataFrame(
    results
)

meta.to_csv(
    METADATA_FILE,
    index=False
)

print("\nFinished\n")

print(
    meta["success"]
    .value_counts()
)

print(
    "\nSaved metadata:"
)

print(METADATA_FILE)

print(
    "\nTranscript statistics:"
)

print(
    meta[
        [
            "language",
            "generated",
            "segments",
            "words",
            "characters"
        ]
    ]
)
