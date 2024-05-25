import os
import json

SAVE_SLOTS = 3
SAVE_DIR = "saves"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def save_game(character, slot):
    if slot < 1 or slot > SAVE_SLOTS:
        print("Invalid save slot.")
        return

    save_data = {
        "character": character.to_dict(),
        "slot": slot
    }

    save_path = os.path.join(SAVE_DIR, f"save_slot_{slot}.json")
    with open(save_path, "w") as f:
        json.dump(save_data, f, indent=4, default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else o)
    print(f"Game saved to slot {slot}.")

def load_game(slot):
    if slot < 1 or slot > SAVE_SLOTS:
        print("Invalid save slot.")
        return None

    save_path = os.path.join(SAVE_DIR, f"save_slot_{slot}.json")
    if not os.path.exists(save_path):
        print(f"No save file found in slot {slot}.")
        return None

    with open(save_path, "r") as f:
        data = json.load(f)
        character_data = data["character"]
        from characters.character import Character
        character = Character.from_dict(character_data)
        print(f"Game loaded from slot {slot}.")
        return character
