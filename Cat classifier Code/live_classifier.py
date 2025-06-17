# live_classifier.py

import cv2
import torch
import torch.nn.functional as F
from torchvision import models, transforms
import argparse
import time
from PIL import Image

# ✅ Load EfficientNetB0 model
def load_efficientnet_model(model_path, num_classes):
    model = models.efficientnet_b0(pretrained=False)
    model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    return model

# ✅ Main live classifier
def run_live_classifier(model, class_names, device, camera_id=0):
    # Open webcam
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"Error: Could not open webcam (ID {camera_id})")
        return
    
    print(f"Webcam opened successfully (ID {camera_id})")
    print("Press 'q' to quit")

    # Define transforms (match your validation transforms)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Convert to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)

            # Preprocess
            input_tensor = transform(pil_image).unsqueeze(0).to(device)

            # Inference
            with torch.no_grad():
                start_time = time.time()
                output = model(input_tensor)
                inference_time = time.time() - start_time

                probs = F.softmax(output, dim=1)
                confidence, pred_idx = torch.max(probs, 1)

            class_name = class_names[pred_idx.item()]
            confidence_pct = confidence.item() * 100

            # Display result on frame
            display_text = f"{class_name} ({confidence_pct:.2f}%) - {inference_time*1000:.1f}ms"
            cv2.putText(frame, display_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Show frame
            cv2.imshow('Live Cat Breed Classifier', frame)

            # Press 'q' to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam closed")

# ✅ Main entry point
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Live Cat Breed Classifier')
    parser.add_argument('--model', type=str, required=True,
                        help='Path to model .pt file (e.g., efficientnet_s4_best.pt)')
    parser.add_argument('--class_file', type=str, required=True,
                        help='Path to classes.txt file')
    parser.add_argument('--camera', type=int, default=0,
                        help='Webcam camera ID (default: 0)')
    args = parser.parse_args()

    # Load class names
    with open(args.class_file, 'r') as f:
        class_names = [line.strip() for line in f.readlines()]
    
    num_classes = len(class_names)
    print(f"Loaded {num_classes} classes")

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Load model
    model = load_efficientnet_model(args.model, num_classes)
    model.to(device)

    # Run live classifier
    run_live_classifier(model, class_names, device, camera_id=args.camera)
