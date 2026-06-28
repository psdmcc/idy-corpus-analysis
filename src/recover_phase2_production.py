import pandas as pd
from pathlib import Path
import time
import random
import json
from datetime import datetime
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
OUTPUT_DIR = Path("data/transcripts_recovered")
LOG_PATH = Path("data/analysis/recovery_log_production.jsonl")
CHECKPOINT_PATH = Path("data/analysis/recovery_checkpoint_production.json")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# batch control
BATCH_SIZE = 20
REQUEST_DELAY_MIN = 2.0
REQUEST_DELAY_MAX = 5.0

COOLDOWN_SECONDS = 600  # 10 min hard pause on IP block

# =========================
# METRICS
# =========================

metrics = {
    "success": 0,
    "fail": 0,
    "blocked": 0,
    "words": 0,
    "segments": 0
}

# =========================
# UTILITIES
# =========================

def now():
    return datetime.utcnow().isoformat()

def log_event(event: dict):
    event["timestamp"] = now()
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

def save_checkpoint(video_id, index):
    data = {
        "last_video_id": video_id,
        "last_index": index,
        "timestamp": now(),
        "metrics": metrics
    }
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump(data, f, indent=2)

def throttle():
    time.sleep(random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX))

# =========================
# LANGUAGE SELECTION
# =========================

def choose_transcript(transcripts):
    """
    Priority:
    1. manual EN
    2. auto EN
    3. manual HI
    4. auto HI
    5. fallback
    """
    transcripts = list(transcripts)

    for t in transcripts:
        if t.language_code.startswith("en") and not t.is_generated:
            return t

    for t in transcripts:
        if t.language_code.startswith("en") and t.is_generated:
            return t

    for t in transcripts:
        if t.language_code == "hi" and not t.is_generated:
            return t

    for t in transcripts:
        if t.language_code == "hi" and t.is_generated:
            return t

    return transcripts[0]

# =========================
# TRANSCRIPT FETCHER
# =========================

def fetch_transcript(video_id):
    ytt = YouTubeTranscriptApi()

    tl = ytt.list(video_id)
    chosen = choose_transcript(tl)

    data = chosen.fetch()

    text = " ".join([seg.text for seg in data])
    word_count = len(text.split())

    return {
        "language": chosen.language_code,
        "generated": chosen.is_generated,
        "segments": len(data),
        "words": word_count,
        "text": text
    }

# =========================
# PIPELINE WORKER
# =========================

def process_video(video_id, index):
    try:
        throttle()

        result = fetch_transcript(video_id)

        output_file = OUTPUT_DIR / f"{video_id}.{result['language']}.txt"

        with open(output_file, "w") as f:
            f.write(result["text"])

        metrics["success"] += 1
        metrics["words"] += result["words"]
        metrics["segments"] += result["segments"]

        log_event({
            "video_id": video_id,
            "status": "success",
            "language": result["language"],
            "segments": result["segments"],
            "words": result["words"],
            "success": True
        })

        print(f"[{index}] SUCCESS {video_id} | {result['language']} | words={result['words']}")

        return True

    except (IpBlocked, RequestBlocked):
        metrics["blocked"] += 1

        log_event({
            "video_id": video_id,
            "status": "blocked",
            "error": "IpBlocked",
            "success": False
        })

        print(f"[{index}] BLOCKED → cooling down {COOLDOWN_SECONDS}s")
        time.sleep(COOLDOWN_SECONDS)

        return False

    except (NoTranscriptFound, TranscriptsDisabled) as e:
        metrics["fail"] += 1

        log_event({
            "video_id": video_id,
            "status": "fail",
            "error": type(e).__name__,
            "success": False
        })

        print(f"[{index}] FAIL {video_id} | {type(e).__name__}")

        return False

    except Exception as e:
        metrics["fail"] += 1

        log_event({
            "video_id": video_id,
            "status": "fail",
            "error": str(e),
            "success": False
        })

        print(f"[{index}] FAIL {video_id} | {e}")

        return False

# =========================
# MAIN RUNNER
# =========================

def main():
    df = pd.read_csv(QUEUE_PATH)
    video_ids = df["video_id"].tolist()

    print(f"Starting production recovery: {len(video_ids)} videos")

    for i, vid in enumerate(video_ids, start=1):

        success = process_video(vid, i)

        # checkpoint every video (safe for restart)
        save_checkpoint(vid, i)

        # optional early slowdown if instability appears
        if metrics["blocked"] > 0 and metrics["blocked"] % 5 == 0:
            print("Repeated blocking detected → extended cooldown")
            time.sleep(300)

    print("\nFINISHED")
    print(metrics)

    summary = pd.Series({
        "success": metrics["success"],
        "fail": metrics["fail"],
        "blocked": metrics["blocked"],
        "words": metrics["words"],
        "segments": metrics["segments"]
    })

    print(summary)


if __name__ == "__main__":
    main()
