import os

MEMORY_FILE = os.path.join("Permanent memory", "Permanent-memory")

def register_tools(registry):
    registry.register("update_memory", update_memory, "Appends important facts about the user to permanent memory. Arguments: info (str).", requires_context=False)
    registry.register("read_memory", read_memory, "Reads the permanent memory to retrieve stored facts about the user.", requires_context=False)

def ensure_memory_file():
    directory = os.path.dirname(MEMORY_FILE)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            f.write("")

def update_memory(info, **kwargs):
    """Appends important facts about the user to permanent memory."""
    try:
        ensure_memory_file()
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{info}")
        return f"Memory updated: {info}"
    except Exception as e:
        return f"Error updating memory: {str(e)}"

def read_memory(**kwargs):
    """Reads the permanent memory."""
    try:
        ensure_memory_file()
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        return content if content else "Memory is empty."
    except Exception as e:
        return f"Error reading memory: {str(e)}"
