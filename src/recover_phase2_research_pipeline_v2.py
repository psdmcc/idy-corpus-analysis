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
# CONFIG
# =========================

QUEUE_PATH = "data/analysis/transcript_recovery_queue.csv"

OUT_DIR = Path("data/transcripts_recovered_research")
OUT_DIR.mkdir(parents=True, exist_ok=True)

LOG_PATH = Path("data/analysis/recovery_log_research.jsonl")
CHECKPOINT_PATH = Path("data/analysis/recovery_checkpoint_research.json")
DATASET_PATH = Path("data/analysis/final_research_dataset.csv")

BATCH_SIZE = 20

BASE_DELAY = (2.0, 6.0)

# =========================
# METRICS
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

def load_checkpoint():
    if CHECKPOINT_PATH.exists():
        with open(CHECKPOINT_PATH) as f:
            data = json.load(f)
        return data.get("index", 0), data.get("block_count", 0)
    return 0, 0

def checkpoint(video_id, idx, block_count):
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump({
            "last_video_id": video_id,
            "index": idx,
            "block_count": block_count,
            "timestamp": now(),
            "metrics": dict(metrics)
        }, f, indent=2)

# =========================
# ADAPTIVE THROTTLING (KEY UPGRADE)
# =========================

def adaptive_sleep(block_count):
    base = random.uniform(*BASE_DELAY)
    penalty = block_count * 0.7
    return base + penalty

def adaptive_cooldown(block_count):
    return min(1800, 300 * (2 ** block_count))

# =========================
# LANGUAGE SELECTION
# =========================

def choose_transcript(transcripts):
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
# TRANSCRIPT FETCH
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
# PROCESSOR (CORE LOGIC)
# =========================

def process(video_id, i, block_count):
    try:
        time.sleep(adaptive_sleep(block_count))

        result = fetch_transcript(video_id)

        out_file = OUT_DIR / f"{video_id}.{result['language']}.txt"
        out_file.write_text(result["text"])

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

        return result, block_count

    except (IpBlocked, RequestBlocked):
        metrics["blocked"] += 1
        metrics["error_distribution"]["IpBlocked"] += 1

        block_count += 1

        cooldown = adaptive_cooldown(block_count)

        log({
            "video_id": video_id,
            "status": "blocked",
            "cooldown": cooldown
        })

        print(f"[{i}] IP BLOCKED → cooling {cooldown}s (block_count={block_count})")

        time.sleep(cooldown)

        return None, block_count

    except (NoTranscriptFound, TranscriptsDisabled) as e:
        metrics["fail"] += 1
        metrics["error_distribution"][type(e).__name__] += 1

        log({
            "video_id": video_id,
            "status": "fail",
            "error": type(e).__name__
        })

        print(f"[{i}] FAIL | {video_id} | {type(e).__name__}")

        return None, block_count

    except Exception as e:
        metrics["fail"] += 1
        metrics["error_distribution"]["Other"] += 1

        log({
            "video_id": video_id,
            "status": "fail",
            "error": str(e)
        })

        print(f"[{i}] FAIL | {video_id} | {e}")

        return None, block_count

# =========================
# EXPORT
# =========================

def export_dataset():
    logs = []

    with open(LOG_PATH) as f:
        for line in f:
            logs.append(json.loads(line))

    df = pd.DataFrame(logs)

    if "words" in df.columns:
        df["is_long_form"] = df["words"] > 1000
        df["density"] = df["words"] / df["segments"].replace(0, 1)

    df.to_csv(DATASET_PATH, index=False)

    print("\nDATASET SAVED:", DATASET_PATH)

# =========================
# MAIN RUNNER (FIXED + RESUME SAFE)
# =========================

def main():
    df = pd.read_csv(QUEUE_PATH)
    videos = df["video_id"].tolist()

    start_index, block_count = load_checkpoint()

    print(f"Resuming from index: {start_index}")
    print(f"Total videos: {len(videos)}")
    print(f"Initial block_count: {block_count}")

    for i, vid in enumerate(videos[start_index:], start=start_index + 1):

        result, block_count = process(vid, i, block_count)

        checkpoint(vid, i, block_count)

        # safety break if system is unstable
        if block_count >= 5:
            print("⚠️ Too many IP blocks — pausing pipeline safely")
            break

    print("\nFINAL METRICS:")
    print(metrics)

    export_dataset()

    print("\nPIPELINE COMPLETE")

# =========================
# ENTRY
# =========================

if __name__ == "__main__":
    main()
