import pandas as pd
from pathlib import Path
import time
import random
import json
from datetime import datetime
from collections import Counter

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    IpBlocked,
    RequestBlocked
)

# =========================
# CONFIGURATION
# =========================

QUEUE_PATH = "data/analysis/transcript_recovery_queue.csv"

OUT_DIR = Path("data/transcripts_recovered_research")
OUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_PATH = Path("data/analysis/recovery_log_research.jsonl")
CHECKPOINT_PATH = Path("data/analysis/recovery_checkpoint_research.json")
DATASET_PATH = Path("data/analysis/final_research_dataset.csv")

BATCH_SIZE = 10
DELAY_RANGE = (5.0, 10.0)
COOLDOWN = 300

# =========================
# METRICS (RESEARCH LAYER)
# =========================

metrics = {
    "success": 0,
    "fail": 0,
    "blocked": 0,
    "total_words": 0,
    "total_segments": 0,
    "language_distribution": Counter(),
    "error_distribution": Counter()
}

# =========================
# UTILITIES
# =========================

def now():
    return datetime.utcnow().isoformat()

def log(event):
    event["timestamp"] = now()
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

def checkpoint(video_id, idx):
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump({
            "last_video_id": video_id,
            "index": idx,
            "timestamp": now(),
            "metrics": dict(metrics)
        }, f, indent=2)

def throttle():
    time.sleep(random.uniform(*DELAY_RANGE))

# =========================
# LANGUAGE SELECTION POLICY
# =========================

def choose_transcript(transcripts):
    """
    Research policy prioritisation:
    1. Human English
    2. Auto English
    3. Human Hindi
    4. Auto Hindi
    5. Best available fallback
    """

    transcripts = list(transcripts)

    def pick(lang, generated):
        for t in transcripts:
            if t.language_code.startswith(lang) and t.is_generated == generated:
                return t
        return None

    return (
        pick("en", False)
        or pick("en", True)
        or pick("hi", False)
        or pick("hi", True)
        or transcripts[0]
    )

# =========================
# TRANSCRIPT PROCESSING
# =========================

def fetch_transcript(video_id):
    ytt = YouTubeTranscriptApi()
    transcript_list = ytt.list(video_id)

    chosen = choose_transcript(transcript_list)
    data = chosen.fetch()

    text = " ".join([s.text for s in data])
    words = len(text.split())

    return {
        "video_id": video_id,
        "language": chosen.language_code,
        "generated": chosen.is_generated,
        "segments": len(data),
        "words": words,
        "text": text
    }

# =========================
# PIPELINE CORE
# =========================

def process(video_id, i):
    try:
        throttle()

        result = fetch_transcript(video_id)

        # save raw transcript
        out_file = OUT_DIR / f"{video_id}.{result['language']}.txt"
        out_file.write_text(result["text"])

        # update metrics
        metrics["success"] += 1
        metrics["total_words"] += result["words"]
        metrics["total_segments"] += result["segments"]
        metrics["language_distribution"][result["language"]] += 1

        log({
            "video_id": video_id,
            "status": "success",
            **result
        })

        print(f"[{i}] SUCCESS | {video_id} | {result['language']} | words={result['words']}")
        return result

    except (IpBlocked, RequestBlocked):
        metrics["blocked"] += 1
        metrics["error_distribution"]["IpBlocked"] += 1

        log({
            "video_id": video_id,
            "status": "blocked",
            "error": "IpBlocked"
        })

        print(f"[{i}] IP BLOCKED → cooling {COOLDOWN}s")
        time.sleep(COOLDOWN)

        return None

    except (NoTranscriptFound, TranscriptsDisabled) as e:
        metrics["fail"] += 1
        metrics["error_distribution"][type(e).__name__] += 1

        log({
            "video_id": video_id,
            "status": "fail",
            "error": type(e).__name__
        })

        print(f"[{i}] FAIL | {video_id} | {type(e).__name__}")
        return None

    except Exception as e:
        metrics["fail"] += 1
        metrics["error_distribution"]["Other"] += 1

        log({
            "video_id": video_id,
            "status": "fail",
            "error": str(e)
        })

        print(f"[{i}] FAIL | {video_id} | {e}")
        return None

# =========================
# FINAL DATASET EXPORT
# =========================

def export_dataset():
    log_data = []

    with open(LOG_PATH) as f:
        for line in f:
            log_data.append(json.loads(line))

    df = pd.DataFrame(log_data)

    if "words" not in df.columns:
        print("No usable dataset yet")
        return

    # research-grade enrichment
    df["is_long_form"] = df["words"] > 1000
    df["density"] = df["words"] / df["segments"].replace(0, 1)

    df.to_csv(DATASET_PATH, index=False)

    print("\nDATASET SAVED:")
    print(DATASET_PATH)

# =========================
# MAIN RUNNER
# =========================

def load_checkpoint():
    if CHECKPOINT_PATH.exists():
        with open(CHECKPOINT_PATH) as f:
            data = json.load(f)
        return data.get("index", 0)
    return 0


def main():
    df = pd.read_csv(QUEUE_PATH)
    videos = df["video_id"].tolist()

    start_index = load_checkpoint()

    print(f"Resuming from index: {start_index}")
    print(f"Total videos: {len(videos)}")

    for i, vid in enumerate(videos[start_index:], start=start_index + 1):

        process(vid, i)
        checkpoint(vid, i)

        if metrics["blocked"] > 0:
            print("BLOCK DETECTED → cooling + pausing pipeline state")
            time.sleep(COOLDOWN)

    print("\nFINAL METRICS")
    print(metrics)

    export_dataset()

# =========================
# ENTRY
# =========================

if __name__ == "__main__":
    main()
