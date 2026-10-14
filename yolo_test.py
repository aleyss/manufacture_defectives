from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Check model path in models/ or weights/
model_path = os.path.join(BASE_DIR, "models", "best.pt")
if not os.path.exists(model_path):
    model_path = os.path.join(BASE_DIR, "weights", "best.pt")

test_folder = os.path.join(BASE_DIR, "test_folder")

model = YOLO(model_path)

print("====================================")
print("6-CLASS PCB MODEL TEST")
print("====================================")

print("\nLoaded Model Classes:")
for k, v in model.names.items():
    print(f"  {k}: {v}")

images = [
    os.path.join(test_folder, file)
    for file in os.listdir(test_folder)
    if file.lower().endswith((".jpg", ".jpeg", ".png"))
][:10]

print(f"\nTesting {len(images)} images from {test_folder}...\n")

for image in images:
    results = model.predict(
        source=image,
        conf=0.10,
        verbose=False
    )

    print("------------------------------------")
    print("Image:", os.path.basename(image))

    detected = False

    for result in results:
        if result.boxes is None or len(result.boxes) == 0:
            continue

        detected = True

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_id]

            print(
                f"  -> Detected: [{class_id}] {class_name} | "
                f"Confidence: {confidence * 100:.2f}%"
            )

    if not detected:
        print("  -> No defect detected.")