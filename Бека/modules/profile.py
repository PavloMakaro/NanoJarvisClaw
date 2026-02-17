import json
import os

PROFILE_FILE = "data/profiles.json"

def register_tools(registry):
    registry.register("set_profile_info", set_profile_info, "Saves user profile information. Arguments: key (str), value (str).", requires_context=True)
    registry.register("get_profile_info", get_profile_info, "Gets user profile information. Arguments: key (str).", requires_context=True)
    registry.register("get_full_profile", get_full_profile, "Gets the full user profile.", requires_context=True)

def load_profiles():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_profiles(profiles):
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(PROFILE_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

def set_profile_info(key, value, chat_id=None, **kwargs):
    """Saves user profile information."""
    if not chat_id:
        return "Error: No chat_id provided."

    chat_id = str(chat_id)
    profiles = load_profiles()

    if chat_id not in profiles:
        profiles[chat_id] = {}

    profiles[chat_id][key] = value
    save_profiles(profiles)
    return f"Saved {key}: {value}"

def get_profile_info(key, chat_id=None, **kwargs):
    """Gets user profile information."""
    if not chat_id:
        return "Error: No chat_id provided."

    chat_id = str(chat_id)
    profiles = load_profiles()

    user_profile = profiles.get(chat_id, {})
    return user_profile.get(key, f"Info '{key}' not set.")

def get_full_profile(chat_id=None, **kwargs):
    """Gets the full user profile."""
    if not chat_id:
        return "Error: No chat_id provided."

    chat_id = str(chat_id)
    profiles = load_profiles()

    return json.dumps(profiles.get(chat_id, {}), indent=2)
