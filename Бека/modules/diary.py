import os
import datetime

def register_tools(registry):
    registry.register("add_diary_entry", add_entry, "Adds a new entry to the user diary. Arguments: text (str).")
    registry.register("read_diary", read_entries, "Reads diary entries. Arguments: date (str, optional, YYYY-MM-DD).")
    registry.register("setup_diary_reminder", setup_reminder, "Sets up a daily diary reminder. Arguments: time (str, e.g., '20:00').", requires_context=True)

def add_entry(text):
    """Adds a diary entry."""
    if not os.path.exists("data"):
        os.makedirs("data")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {text}\n"

    try:
        with open("data/diary.txt", "a", encoding="utf-8") as f:
            f.write(entry)
        return "Diary entry added."
    except Exception as e:
        return f"Error writing to diary: {str(e)}"

def read_entries(date=None):
    """Reads diary entries."""
    if not os.path.exists("data/diary.txt"):
        return "Diary is empty."

    try:
        with open("data/diary.txt", "r", encoding="utf-8") as f:
            content = f.read()

        if date:
            # Simple filter by string matching the date
            filtered = [line for line in content.splitlines() if line.startswith(f"[{date}")]
            return "\n".join(filtered) if filtered else f"No entries found for {date}."

        return content[-2000:] + "\n...(showing last 2000 chars)" if len(content) > 2000 else content
    except Exception as e:
        return f"Error reading diary: {str(e)}"

async def diary_alarm(context):
    """Callback function for the diary alarm job."""
    job = context.job
    # Check if entry made today? (Simplified: Just prompt)
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # Check if we have an entry for today
    has_entry = False
    if os.path.exists("data/diary.txt"):
        with open("data/diary.txt", "r", encoding="utf-8") as f:
            if today in f.read():
                has_entry = True

    if not has_entry:
        await context.bot.send_message(job.chat_id, text="📓 DIARY PROMPT: You haven't written in your diary today. How was your day? (Reply with voice or text)")
    else:
        # Maybe a gentle "Anything else?" or nothing.
        pass

async def setup_reminder(time_str="20:00", job_queue=None, chat_id=None, **kwargs):
    """Sets up a daily diary reminder."""
    if not job_queue or not chat_id:
        return "Error: JobQueue or ChatID missing."

    try:
        hour, minute = map(int, time_str.split(":"))
        t = datetime.time(hour=hour, minute=minute)

        # job_queue.run_daily(diary_alarm, t, chat_id=chat_id, name=f"diary_{chat_id}")
        job_queue.run_daily(diary_alarm, t, chat_id=chat_id, name=f"diary_{chat_id}")
        return f"Daily diary reminder set for {time_str}."
    except Exception as e:
        return f"Error setting reminder: {str(e)}"
