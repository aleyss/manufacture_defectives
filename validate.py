from ultralytics import YOLO

model_path = r"C:\Users\alekhya\OneDrive\Desktop\proj\manufacture_defectives\models\best.pt"

model = YOLO(model_path)

print("Running validation...")

metrics = model.val(
    data="data.yaml",
    split="val",
    imgsz=320,
    batch=8,
    device="cpu"
)

print("\n========== MODEL PERFORMANCE ==========")
print("Precision :", metrics.box.mp)
print("Recall    :", metrics.box.mr)
print("mAP50     :", metrics.box.map50)
print("mAP50-95  :", metrics.box.map)