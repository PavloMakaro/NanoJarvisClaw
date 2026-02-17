import os
from core.memory_rag import memory_instance

# Still keep the old file as backup or for migration if needed
MEMORY_FILE = os.path.join("Permanent memory", "Permanent-memory")

def register_tools(registry):
    registry.register("update_memory", update_memory, "Appends important facts about the user to permanent memory (Vector DB). Arguments: info (str).", requires_context=False)
    registry.register("read_memory", read_memory, "Retrieves relevant facts from memory using vector search. Arguments: query (str).", requires_context=False)

def update_memory(info, **kwargs):
    """Appends important facts about the user to permanent memory."""
    # Try Vector Memory first
    if memory_instance.enabled:
        res = memory_instance.add(info)
        return f"Memory updated (Vector): {res}"

    # Fallback to file
    try:
        ensure_memory_file()
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{info}")
        return f"Memory updated (File - Legacy): {info}"
    except Exception as e:
        return f"Error updating memory: {str(e)}"

def read_memory(query=None, **kwargs):
    """Retrieves relevant facts from memory."""
    # If query is provided, use vector search
    if query and memory_instance.enabled:
        results = memory_instance.search(query, n_results=3)
        if results:
            formatted = "\n".join([f"- {r}" for r in results])
            return f"Relevant Memory:\n{formatted}"
        else:
            return "No relevant memory found."

    # Fallback: Read full file (discouraged but available if no query or no vector)
    try:
        ensure_memory_file()
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        return content if content else "Memory is empty."
    except Exception as e:
        return f"Error reading memory: {str(e)}"

def ensure_memory_file():
    directory = os.path.dirname(MEMORY_FILE)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            f.write("")
