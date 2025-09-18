import os

# --- CONFIGURATION ---
# This path is now updated with your folder name.
DATASET_ROOT_PATH = "../datasets/char_detection_dataset"

# The original, messy list of 158 classes from your first download.
OLD_NAMES = ['Ally Barbarian', 'Ally Barbarian Barrel', 'Ally Battle Ram', 'Ally Bomber', 'Ally Evo Firecracker', 'Ally Evo Valkeryie', 'Ally Executioner', 'Ally Firecracker', 'Ally Fisherman', 'Ally Goblin', 'Ally Goblin Barrel', 'Ally Goblin Brawler', 'Ally Goblin Cage', 'Ally Knight', 'Ally Magic Archerer', 'Ally Mini Pekka', 'Ally Minion', 'Ally Pekka', 'Ally Prince', 'Ally Ram Rider', 'Ally Skeleton', 'Ally Spear Goblin', 'Ally Tombstone', 'Ally Valkeyrie', 'Enemy -C- Cannon cart', 'Enemy -C- Cannon cart S2', 'Enemy -C-Monk', 'Enemy Archerer', 'Enemy Archerer Queen Invis', 'Enemy Archerer Queen Visible', 'Enemy Arrow', 'Enemy Baby Dragon', 'Enemy Balloon', 'Enemy Bandit', 'Enemy Barbarian', 'Enemy Barbarian Hut', 'Enemy Bat', 'Enemy Battle Healer', 'Enemy Battle Ram', 'Enemy Bomb Tower', 'Enemy Bowler', 'Enemy Cannon', 'Enemy Cannon cart', 'Enemy Cannon cart s2', 'Enemy Closed Tesla', 'Enemy Dark Prince', 'Enemy Dart Goblin', 'Enemy Death Bomb', 'Enemy EGiant', 'Enemy Earthquake', 'Enemy Ebarbs', 'Enemy Electro Dragon', 'Enemy Elixer Icon 0', 'Enemy Elixer Icon 0.5', 'Enemy Elixer Icon 1', 'Enemy Elixer Pump', 'Enemy Elixir Blob', 'Enemy Elixir Golem', 'Enemy Elixir golem Mini Man', 'Enemy Espirit', 'Enemy Evo Archerers', 'Enemy Evo Barbarians', 'Enemy Evo Bat', 'Enemy Evo Bomber', 'Enemy Evo Firecracker', 'Enemy Evo Knight', 'Enemy Evo Mortar', 'Enemy Evo Recruit', 'Enemy Evo Royal Giant', 'Enemy Evo Skeleton', 'Enemy Evo Valkeryie', 'Enemy Evo Wall-breakers', 'Enemy Ewiz', 'Enemy Executioner', 'Enemy Fire Spirit', 'Enemy Fireball', 'Enemy Firecracker', 'Enemy Fisherman', 'Enemy Flying Machine', 'Enemy Freeze', 'Enemy Furnace', 'Enemy Giant', 'Enemy Giant Skeleton', 'Enemy Goblin', 'Enemy Goblin Brawler', 'Enemy Goblin Cage', 'Enemy Goblin Drill', 'Enemy Goblin Giant', 'Enemy Goblin Hut', 'Enemy Golden Night', 'Enemy Golem', 'Enemy Golemet', 'Enemy Graveyard', 'Enemy Guard', 'Enemy Heal Spirit', 'Enemy Hog Rider', 'Enemy Hunter', 'Enemy Ice Golem', 'Enemy Ice Wizard', 'Enemy Inferno Dragon', 'Enemy Inferno Tower', 'Enemy Ispirit', 'Enemy Knight', 'Enemy Lavahound', 'Enemy Lavapups', 'Enemy Lightning', 'Enemy Little Prince', 'Enemy Little Prince Guardian', 'Enemy Log', 'Enemy Lumberjack', 'Enemy Magic Archerer', 'Enemy Mega Knight', 'Enemy Mega Minion', 'Enemy Mighty Miner', 'Enemy Miner', 'Enemy Mini Pekka', 'Enemy Minion', 'Enemy Monk', 'Enemy Monk Meditate', 'Enemy Mortar', 'Enemy Mother Witch', 'Enemy Mother Witch Piggies', 'Enemy Musketeer', 'Enemy Night Witch', 'Enemy Open Tesla', 'Enemy Pekka', 'Enemy Phoenix', 'Enemy Phoenix Egg', 'Enemy Poison', 'Enemy Prince', 'Enemy Princess', 'Enemy Rage', 'Enemy Ram Rider', 'Enemy Rascal Boy', 'Enemy Rascal Slinger', 'Enemy Rocket', 'Enemy Royal Giant', 'Enemy Royal Pigs', 'Enemy Royal Recruit', 'Enemy Royale Ghost', 'Enemy Royale Ghost Visible', 'Enemy Skeleton', 'Enemy Skeleton Barrel', 'Enemy Skeleton Dragons', 'Enemy Skeleton King', 'Enemy Snowball', 'Enemy Sparky', 'Enemy Spear Goblin', 'Enemy Tombstone', 'Enemy Tornado', 'Enemy Valkeyrie', 'Enemy Wall-braker', 'Enemy Wizard', 'Enemy XBow', 'Enemy Zappy', 'Zap', 'ebar', 'knight']


# The new, cleaned list of 156 classes.
NEW_NAMES = ['Ally_Barbarian', 'Ally_Barbarian_Barrel', 'Ally_Battle_Ram', 'Ally_Bomber', 'Ally_Evo_Firecracker', 'Ally_Evo_Valkyrie', 'Ally_Executioner', 'Ally_Firecracker', 'Ally_Fisherman', 'Ally_Goblin', 'Ally_Goblin_Barrel', 'Ally_Goblin_Brawler', 'Ally_Goblin_Cage', 'Ally_Knight', 'Ally_Magic_Archer', 'Ally_Mini_Pekka', 'Ally_Minion', 'Ally_Pekka', 'Ally_Prince', 'Ally_Ram_Rider', 'Ally_Skeleton', 'Ally_Spear_Goblin', 'Ally_Tombstone', 'Ally_Valkyrie', 'Enemy_Cannon_Cart', 'Enemy_Cannon_Cart_S2', 'Enemy_Monk', 'Enemy_Archer', 'Enemy_Archer_Queen_Invis', 'Enemy_Archer_Queen_Visible', 'Enemy_Arrow', 'Enemy_Baby_Dragon', 'Enemy_Balloon', 'Enemy_Bandit', 'Enemy_Barbarian', 'Enemy_Barbarian_Hut', 'Enemy_Bat', 'Enemy_Battle_Healer', 'Enemy_Battle_Ram', 'Enemy_Bomb_Tower', 'Enemy_Bowler', 'Enemy_Cannon', 'Enemy_Cannon_Cart', 'Enemy_Cannon_Cart_S2', 'Enemy_Closed_Tesla', 'Enemy_Dark_Prince', 'Enemy_Dart_Goblin', 'Enemy_Death_Bomb', 'Enemy_EGiant', 'Enemy_Earthquake', 'Enemy_Ebarbs', 'Enemy_Electro_Dragon', 'Enemy_Elixir_Icon_0', 'Enemy_Elixir_Icon_0.5', 'Enemy_Elixir_Icon_1', 'Enemy_Elixir_Pump', 'Enemy_Elixir_Blob', 'Enemy_Elixir_Golem', 'Enemy_Elixir_Golemite', 'Enemy_Espirit', 'Enemy_Evo_Archer', 'Enemy_Evo_Barbarians', 'Enemy_Evo_Bat', 'Enemy_Evo_Bomber', 'Enemy_Evo_Firecracker', 'Enemy_Evo_Knight', 'Enemy_Evo_Mortar', 'Enemy_Evo_Recruit', 'Enemy_Evo_Royal_Giant', 'Enemy_Evo_Skeleton', 'Enemy_Evo_Valkyrie', 'Enemy_Evo_WallBreaker', 'Enemy_Ewiz', 'Enemy_Executioner', 'Enemy_Fire_Spirit', 'Enemy_Fireball', 'Enemy_Firecracker', 'Enemy_Fisherman', 'Enemy_Flying_Machine', 'Enemy_Freeze', 'Enemy_Furnace', 'Enemy_Giant', 'Enemy_Giant_Skeleton', 'Enemy_Goblin', 'Enemy_Goblin_Brawler', 'Enemy_Goblin_Cage', 'Enemy_Goblin_Drill', 'Enemy_Goblin_Giant', 'Enemy_Goblin_Hut', 'Enemy_Golden_Knight', 'Enemy_Golem', 'Enemy_Golemite', 'Enemy_Graveyard', 'Enemy_Guard', 'Enemy_Heal_Spirit', 'Enemy_Hog_Rider', 'Enemy_Hunter', 'Enemy_Ice_Golem', 'Enemy_Ice_Wizard', 'Enemy_Inferno_Dragon', 'Enemy_Inferno_Tower', 'Enemy_Ispirit', 'Enemy_Knight', 'Enemy_Lavahound', 'Enemy_Lavapup', 'Enemy_Lightning', 'Enemy_Little_Prince', 'Enemy_Little_Prince_Guardian', 'Enemy_Log', 'Enemy_Lumberjack', 'Enemy_Magic_Archer', 'Enemy_Mega_Knight', 'Enemy_Mega_Minion', 'Enemy_Mighty_Miner', 'Enemy_Miner', 'Enemy_Mini_Pekka', 'Enemy_Minion', 'Enemy_Monk', 'Enemy_Monk_Meditate', 'Enemy_Mortar', 'Enemy_Mother_Witch', 'Enemy_Mother_Witch_Piggy', 'Enemy_Musketeer', 'Enemy_Night_Witch', 'Enemy_Open_Tesla', 'Enemy_Pekka', 'Enemy_Phoenix', 'Enemy_Phoenix_Egg', 'Enemy_Poison', 'Enemy_Prince', 'Enemy_Princess', 'Enemy_Rage', 'Enemy_Ram_Rider', 'Enemy_Rascal_Boy', 'Enemy_Rascal_Slinger', 'Enemy_Rocket', 'Enemy_Royal_Giant', 'Enemy_Royal_Pig', 'Enemy_Royal_Recruit', 'Enemy_Royale_Ghost', 'Enemy_Royale_Ghost_Visible', 'Enemy_Skeleton', 'Enemy_Skeleton_Barrel', 'Enemy_Skeleton_Dragon', 'Enemy_Skeleton_King', 'Enemy_Snowball', 'Enemy_Sparky', 'Enemy_Spear_Goblin', 'Enemy_Tombstone', 'Enemy_Tornado', 'Enemy_Valkyrie', 'Enemy_WallBreaker', 'Enemy_Wizard', 'Enemy_XBow', 'Enemy_Zappy', 'Zap']


# --- SCRIPT LOGIC (No need to edit below this line) ---

def create_class_map(old_list, new_list):
    """Creates a mapping from old class index to new class index."""
    mapping = {}
    new_list_lookup = {name: i for i, name in enumerate(new_list)}

    # A simple cleanup function to normalize names for matching
    def normalize_name(name):
        return name.replace(' ', '_').replace('-C-', '').replace('(C)', '').replace('_', '').replace('Valkeryie',
                                                                                                     'Valkyrie').replace(
            'Archerer', 'Archer').replace('Wall-braker', 'WallBreaker').replace('Golden Night', 'GoldenKnight').replace(
            'Golemet', 'Golemite').lower()

    # Create a lookup for normalized new names
    normalized_new_lookup = {normalize_name(name): i for i, name in enumerate(new_list)}

    for i, old_name in enumerate(old_list):
        normalized_old = normalize_name(old_name)
        if normalized_old in normalized_new_lookup:
            mapping[i] = normalized_new_lookup[normalized_old]
        # Handle special cases like 'ebar' -> 'Ebarbs'
        elif old_name == 'ebar':
            mapping[i] = new_list_lookup.get('Enemy_Ebarbs')

    print("Generated class map. Some classes may be unmapped if they were removed.")
    return mapping


def update_label_files(directory, class_map):
    """Updates all .txt label files in a directory based on the class map."""
    label_dir = os.path.join(directory, 'labels')
    if not os.path.isdir(label_dir):
        print(f"Warning: Label directory not found at {label_dir}")
        return

    print(f"Processing directory: {label_dir}")
    file_count = 0
    updated_line_count = 0

    for filename in os.listdir(label_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(label_dir, filename)

            with open(file_path, 'r') as f:
                lines = f.readlines()

            new_lines = []
            file_updated = False
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue

                try:
                    old_class_id = int(parts[0])
                    if old_class_id in class_map:
                        new_class_id = class_map[old_class_id]
                        new_line = f"{new_class_id} {' '.join(parts[1:])}\n"
                        new_lines.append(new_line)
                        if new_class_id != old_class_id:
                            updated_line_count += 1
                    # If old_class_id is not in the map, it's from a removed class, so we drop it.
                except (ValueError, IndexError):
                    print(f"  - Warning: Skipping malformed line in {filename}: {line.strip()}")
                    continue

            # Only write back to the file if there are lines to write
            if new_lines:
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)
            else:  # If all lines were from removed classes, the file becomes empty
                open(file_path, 'w').close()

            file_count += 1
            if file_count % 500 == 0:
                print(f"  ...processed {file_count} files.")

    print(f"Finished processing {file_count} files in {label_dir}.")
    print(f"Total lines re-mapped: {updated_line_count}")


if __name__ == "__main__":
    if not os.path.isdir(DATASET_ROOT_PATH):
        print(f"Error: The dataset path '{DATASET_ROOT_PATH}' does not exist.")
        print("Please make sure the script is in the same parent directory as your dataset folder.")
    else:
        class_mapping = create_class_map(OLD_NAMES, NEW_NAMES)

        dirs_to_process = [
            os.path.join(DATASET_ROOT_PATH, 'train'),
            os.path.join(DATASET_ROOT_PATH, 'valid'),
            os.path.join(DATASET_ROOT_PATH, 'test')
        ]

        for d in dirs_to_process:
            if os.path.isdir(d):
                update_label_files(d, class_mapping)
            else:
                print(f"Warning: Directory not found, skipping: {d}")

        print("\nLabel re-mapping process complete!")