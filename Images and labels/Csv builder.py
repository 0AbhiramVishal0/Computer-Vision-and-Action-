import os
import pandas as pd

base_path = 'All_Breeds_Dataset/'

# Static Mapping: Breed Name -> Coat Length & Personality
breed_info = {
    "Abyssinian": ("ShortHair", "Busy, active, agenda-driven and affectionate"),
    "American_Shorthair": ("Shorthair", "Even temperament"),
    "Balinese": ("Longhair", "Vocal, affectionate, active"),
    "Bengal": ("Shorthair", "Curious and athletic"),
    "Birman": ("Longhair", "Sweet and affectionate"),
    "British_Shorthair": ("Shorthair", "Calm and quiet; enjoy people"),
    "Burmese": ("Shorthair", "People oriented, affectionate"),
    "Cornish_Rex": ("Shorthair", "Active, racy, affectionate"),
    "Devon_Rex": ("Shorthair", "Pixie like and personality"),
    "Egyptian_Mau": ("Shorthair", "Athletic and active"),
    "Exotic": ("Longhair and Shorthair", "Sweet, affectionate, quiet"),
    "Japanese_Bobtail": ("Longhair and Shorthair", "Active, intelligent, and affectionate"),
    "Maine_Coon_Cat": ("Longhair", "Gentle, easy going yet active"),
    "Norwegian_Forest_Cat": ("Longhair", "Active and sweet"),
    "Oriental": ("Longhair and Shorthair", "Vocal, affectionate, active; can be insistent"),
    "Persian": ("Longhair", "Sweet, affectionate, quiet"),
    "Ragdoll": ("Longhair", "Docile, placid and affectionate"),
    "Russian_Blue": ("Shorthair", "Graceful, playful and quiet"),
    "Scottish_Fold": ("Longhair and Shorthair", "Affectionate and laid back; sweet expressions"),
    "Selkirk_Rex": ("Longhair and Shorthair", "Quiet"),
    "Siamese": ("Shorthair", "Vocal, affectionate, active; can be insistent"),
    "Siberian": ("Longhair", "Dog-like, intelligent and devoted"),
    "Sphynx": ("Shorthair", "Active, affectionate")
}

labels_data = []

for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    if os.path.isdir(folder_path):
        breed = folder.replace("_images", "")
        coat, personality = breed_info.get(breed, ("Unknown", "Unknown"))

        for img_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, img_name)
            
            # Remove extension from Image ID
            image_id = os.path.splitext(img_name)[0]

            labels_data.append({
                "Image ID": image_id,
                "Path": img_path,
                "Breed Name": breed.replace("_", " "),
                "Coat Length": coat,
                "Personality": personality
            })

df = pd.DataFrame(labels_data)
df.to_csv("final_labels.csv", index=False)

print("✅ Labels CSV Generated: final_labels.csv without extensions in Image ID")
