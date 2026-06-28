def assign_ontology(row):
    vid = row["video_id"]
    path = row["filepath"]

    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().lower()
    except:
        return ("UNKNOWN", "UNKNOWN")

    if "international day of yoga" in text:
        return ("STATE", "RITUAL_EVENT_STREAM")

    if "united nations" in text:
        return ("UN", "POLICY_DISCOURSE")

    if "yoga sutra" in text:
        return ("PHILOSOPHICAL_INDIVIDUAL", "PHILOSOPHICAL_EXPOSITION")

    return ("UNKNOWN", "UNKNOWN")
