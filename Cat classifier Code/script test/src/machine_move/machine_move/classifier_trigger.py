import os
import time
import torch
import subprocess
from PIL import Image
from datetime import datetime
from torchvision import transforms, models
import torch.nn.functional as F  # for softmax

# ✅ Load model
model_path = os.path.join(os.path.dirname(__file__), "efficientnet_s4_best.pt")
watch_folder = os.path.expanduser("~/script test/images")
log_file = os.path.join(os.path.dirname(__file__), "trigger_log.txt")

# Correct way: load model as EfficientNetB0 and load state_dict
model = models.efficientnet_b0(pretrained=False)
model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, 23)
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

# ✅ Breed labels
breed_labels = [
    'Abyssinian', 'American Shorthair', 'Balinese', 'Bengal', 'Birman',
    'British Shorthair', 'Burmese', 'Cornish Rex', 'Devon Rex', 'Egyptian Mau',
    'Exotic', 'Japanese Bobtail', 'Maine Coon Cat', 'Norwegian Forest Cat',
    'Oriental', 'Persian', 'Ragdoll', 'Russian Blue', 'Scottish Fold',
    'Selkirk Rex', 'Siamese', 'Siberian', 'Sphynx'
]

# ✅ Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# ✅ Log session start
with open(log_file, "a") as f:
    f.write(f"\n--- Trigger session started at {datetime.now()} ---\n")

# ✅ Start moving robot
print("🟢 Starting robot move command...")
subprocess.Popen([
    "ros2", "run", "machine_move", "move",
    "--linear_vel", "0.01",
    "--angular_vel", "0.0"
])

# ✅ Begin monitoring images
print("📡 Watching for new images... will stop if CONFIDENT cat is detected.")

seen = set()
confidence_threshold = 0.45  # 45% confidence threshold

try:
    while True:
        files = sorted(os.listdir(watch_folder))
        for fname in files:
            if fname.endswith(".jpg") and fname not in seen:
                print("🖼️ New image found → analysing...")

                img_path = os.path.join(watch_folder, fname)
                image = Image.open(img_path).convert("RGB")
                tensor = transform(image).unsqueeze(0)

                with torch.no_grad():
                    output = model(tensor)
                    probs = F.softmax(output, dim=1)
                    confidence, pred_idx = torch.max(probs, 1)
                    confidence = confidence.item()
                    breed = breed_labels[pred_idx.item()]

                print(f"🔍 Prediction: {breed} ({confidence * 100:.2f}% confidence)")

                if confidence >= confidence_threshold:
                    print(f"🐱 CONFIDENT Cat Detected: {breed} ➤ Sending STOP command!")
                    subprocess.run(["ros2", "run", "machine_move", "stop"])

                    with open(log_file, "a") as f:
                        f.write(f"[{datetime.now()}] {fname} ➤ STOPPED for: {breed} ({confidence * 100:.2f}%)\n")

                    seen.add(fname)
                    print("✅ Robot stopped. Exiting script.\n")
                    raise KeyboardInterrupt  # Exit after stopping robot

                else:
                    print("🚗 No confident cat detected → keep moving.")
                    with open(log_file, "a") as f:
                        f.write(f"[{datetime.now()}] {fname} ➤ No confident cat detected ({breed}, {confidence * 100:.2f}%)\n")

                seen.add(fname)

        time.sleep(2)

except KeyboardInterrupt:
    print("🛑 Script stopped by user or after cat detection.")
