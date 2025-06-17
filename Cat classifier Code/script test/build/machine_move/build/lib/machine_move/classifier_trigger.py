import os
import time
import torch
import subprocess
from PIL import Image
from datetime import datetime
from torchvision import transforms

# ✅ Setup
model_path = os.path.join(os.path.dirname(__file__), "efficientnet_s4_best.pt")
watch_folder = os.path.join(os.path.dirname(__file__), "../../capture_images/captured_images")
log_file = os.path.join(os.path.dirname(__file__), "trigger_log.txt")

# ✅ Load model
model = torch.load(model_path, map_location="cpu")
model.eval()

# ✅ Breed list
breed_labels = [
    'Abyssinian', 'American Shorthair', 'Balinese', 'Bengal', 'Birman',
    'British Shorthair', 'Burmese', 'Cornish Rex', 'Devon Rex', 'Egyptian Mau',
    'Exotic', 'Japanese Bobtail', 'Maine Coon Cat', 'Norwegian Forest Cat',
    'Oriental', 'Persian', 'Ragdoll', 'Russian Blue', 'Scottish Fold',
    'Selkirk Rex', 'Siamese', 'Siberian', 'Sphynx'
]

# ✅ Preprocess
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ✅ Log
with open(log_file, "a") as f:
    f.write(f"\n--- Trigger session started at {datetime.now()} ---\n")

# ✅ Detection logic
print("📡 Watching for new images...")

seen = set()
try:
    while True:
        for fname in sorted(os.listdir(watch_folder)):
            if fname.endswith(".jpg") and fname not in seen:
                print("🖼️ New image found → analysing cat breed...")
                img_path = os.path.join(watch_folder, fname)
                image = Image.open(img_path).convert("RGB")
                tensor = transform(image).unsqueeze(0)

                with torch.no_grad():
                    output = model(tensor)
                    pred = output.argmax(dim=1).item()
                    breed = breed_labels[pred]

                print(f"🐱 Breed Detected: {breed}")

                # Decide movement
                if breed in ['Bengal', 'Sphynx', 'Siamese']:
                    print("🛑 Sending stop command...")
                    subprocess.run(["ros2", "run", "machine_move", "stop"])
                else:
                    print("🟢 Sending move command...")
                    subprocess.run([
                        "ros2", "run", "machine_move", "move",
                        "--linear_vel", "0.01",
                        "--angular_vel", "0.0"
                    ])

                with open(log_file, "a") as f:
                    f.write(f"[{datetime.now()}] {fname} ➤ {breed}\n")

                seen.add(fname)
                print("✅ Done.\n")
                break  # only process one image, exit

        time.sleep(2)

except KeyboardInterrupt:
    print("🛑 Script interrupted.")
