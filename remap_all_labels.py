import os

# Base dataset directory
BASE_PATH = r"C:/Users/Admin/Desktop/LAU Documents/Semesters/6. Spring 2025/Software Engineering/Project/ai_traffic_system/merged_dataset"

# Folders to remap
SUBSETS = ["train", "valid", "test"]

# Mapping from emergency dataset classes to COCO-compatible IDs
remap = {
    '0': '4',  # ambulance → 4 (COCO car)
    '1': '5',  # fire_truck → 5 (COCO bus)
    '2': '6'   # police_car → 6 (COCO truck)
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
    for subset in SUBSETS:
        label_dir = os.path.join(BASE_PATH, subset, "labels")
        if not os.path.exists(label_dir):
            print(f"[WARNING] Label folder missing: {label_dir}")
            continue

        for filename in os.listdir(label_dir):
            if filename.endswith(".txt"):
                remap_labels_in_file(os.path.join(label_dir, filename))

        print(f"[✔] Labels remapped in: {label_dir}")

if __name__ == "__main__":
    remap_all_labels()
