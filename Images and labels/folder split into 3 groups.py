import os
import pandas as pd
import shutil

# Read Labels CSV
df = pd.read_csv('final_labels.csv')

# Members
members = ['Sadia', 'Subhana', 'Abhi']

# Destination Base Folder
destination_base = 'Data'

# Loop for Each Breed
for breed in df['Breed Name'].unique():
    breed_images = df[df['Breed Name'] == breed].reset_index(drop=True)
    total_images = len(breed_images)
    split_size = total_images // 3

    splits = {
        'Sadia': breed_images.iloc[:split_size],
        'Subhana': breed_images.iloc[split_size:2 * split_size],
        'Abhi': breed_images.iloc[2 * split_size:]
    }

    for member, images in splits.items():
        for _, row in images.iterrows():
            src = row['Path']
            img_name = row['Image ID']

            # Ensure .jpg extension
            if not img_name.endswith('.jpg'):
                img_name += '.jpg'

            dest_dir = os.path.join(destination_base, member, breed)
            os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, img_name)

            if os.path.exists(src):
                shutil.copy(src, dest_path)
            else:
                print(f"Missing Image: {src}")

print("Images copied successfully to 'Data' folder for Sadia, Subhana, and Abhi with .jpg extension!")
