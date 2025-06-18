import os
import time
from datetime import datetime, timedelta

SUMMARY_DIR = "summaries"
MAX_AGE_DAYS = 30

def cleanup_old_files():
    now = time.time()
    cutoff = now - (MAX_AGE_DAYS * 86400)

    if not os.path.exists(SUMMARY_DIR):
        print(f"📂 Directory '{SUMMARY_DIR}' does not exist. Skipping cleanup.")
        return

    deleted = 0
    for filename in os.listdir(SUMMARY_DIR):
        filepath = os.path.join(SUMMARY_DIR, filename)
        if os.path.isfile(filepath):
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
                deleted += 1
                print(f"🗑️ Deleted: {filename}")

    print(f"✅ Cleanup complete. {deleted} file(s) deleted.")

if __name__ == "__main__":
    cleanup_old_files()
