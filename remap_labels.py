import os

# 📁 Path to your emergency vehicle dataset labels
LABEL_DIR = r"C:/Users/Admin/Desktop/LAU Documents/Semesters/6. Spring 2025/Software Engineering/Project/ai_traffic_system/merged_dataset/train/labels"
  # Update for valid/test if needed

# 🔁 Mapping: original → new label index
remap = {
    '0': '4',  # ambulance → 4
    '1': '5',  # fire_truck → 5
    '2': '6'   # police_car → 6
}

def remap_labels_in_file(file_path):
    new_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts and parts[0] in remap:
                parts[0] = remap[parts[0]]
                new_lines.append(' '.join(parts) + '\n')

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

def remap_all_labels():
    if not os.path.exists(LABEL_DIR):
        print(f"[ERROR] Folder not found: {LABEL_DIR}")
        return

    for filename in os.listdir(LABEL_DIR):
        if filename.endswith('.txt'):
            remap_labels_in_file(os.path.join(LABEL_DIR, filename))

    print("[✔] All labels remapped successfully.")

if __name__ == "__main__":
    remap_all_labels()
