import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PCB Defect Detection",
    page_icon="🏭",
    layout="wide"
)


# ============================================================
# MODEL PATH
# ============================================================
model_path = "models/best.pt"


# ============================================================
# LOAD YOLO MODEL
# ============================================================

@st.cache_resource
def load_model():
    return YOLO(model_path)


model = load_model()


# ============================================================
# CLASS NAMES
# ============================================================

# YOLO stores the class names inside the trained model
class_names = model.names


# ============================================================
# HEADER
# ============================================================

st.title("🏭 PCB Manufacturing Defect Detection")

st.write(
    "Upload a PCB image to detect manufacturing defects "
    "using the trained YOLO11n object detection model."
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("📌 Model Information")

st.sidebar.write("**Model:** YOLO11n")
st.sidebar.write("**Task:** Object Detection")
st.sidebar.write("**Input Size:** 320 × 320")

st.sidebar.write(
    f"**Number of Classes:** {len(class_names)}"
)

st.sidebar.subheader("Defect Classes")

for class_id, class_name in class_names.items():

    st.sidebar.write(
        f"{class_id + 1}. {class_name}"
    )


# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.subheader("📊 Model Performance")

st.caption(
    "Performance measured on the validation dataset."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Precision",
    "19.62%"
)

col2.metric(
    "Recall",
    "46.36%"
)

col3.metric(
    "mAP50",
    "16.10%"
)

col4.metric(
    "mAP50-95",
    "8.74%"
)


st.divider()


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📷 Upload PCB Image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# ============================================================
# PROCESS IMAGE
# ============================================================

if uploaded_file is not None:

    # Load uploaded image
    image = Image.open(
        uploaded_file
    ).convert("RGB")


    # ========================================================
    # RUN YOLO PREDICTION
    # ========================================================

    results = model.predict(
        source=image,
        imgsz=320,
        conf=0.25,
        verbose=False
    )


    # First image result
    result = results[0]


    # ========================================================
    # DISPLAY ORIGINAL + DETECTED IMAGE
    # ========================================================

    col1, col2 = st.columns(
        [1, 1]
    )


    # --------------------------------------------------------
    # ORIGINAL IMAGE
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "📷 Uploaded PCB"
        )

        st.image(
            image,
            use_container_width=True
        )


    # --------------------------------------------------------
    # DETECTED IMAGE
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "🔍 Detection Result"
        )

        # Draw bounding boxes
        annotated_image = result.plot()

        # YOLO returns BGR image
        # Convert BGR → RGB
        annotated_image = annotated_image[:, :, ::-1]

        st.image(
            annotated_image,
            use_container_width=True
        )


    # ========================================================
    # DETECTION INFORMATION
    # ========================================================

    st.divider()

    st.subheader(
        "🎯 Detected Defects"
    )


    # Check whether detections exist
    if result.boxes is not None and len(result.boxes) > 0:

        # Class IDs
        class_ids = (
            result.boxes.cls
            .cpu()
            .numpy()
            .astype(int)
        )

        # Confidence values
        confidences = (
            result.boxes.conf
            .cpu()
            .numpy()
        )


        # ----------------------------------------------------
        # DISPLAY EACH DETECTION
        # ----------------------------------------------------

        for i, (
            class_id,
            confidence
        ) in enumerate(
            zip(
                class_ids,
                confidences
            )
        ):

            class_name = class_names[
                int(class_id)
            ]

            st.write(
                f"### Detection {i + 1}"
            )

            st.metric(
                "Defect Class",
                class_name
            )

            st.metric(
                "Prediction Confidence",
                f"{confidence * 100:.2f}%"
            )

            st.progress(
                float(confidence)
            )

            st.divider()


        # ====================================================
        # BEST DETECTION
        # ====================================================

        st.subheader(
            "🏆 Best Detection"
        )

        best_index = int(
            np.argmax(confidences)
        )

        best_class_id = int(
            class_ids[best_index]
        )

        best_class = class_names[
            best_class_id
        ]

        best_confidence = float(
            confidences[best_index]
        )


        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Detected Defect",
            best_class
        )

        col2.metric(
            "Confidence",
            f"{best_confidence * 100:.2f}%"
        )

        col3.metric(
            "Total Detections",
            len(result.boxes)
        )


    else:

        st.warning(
            "⚠️ No defect detected above the "
            "25% confidence threshold."
        )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.subheader(
    "ℹ️ About the Model"
)

st.write(
    """
    This application uses a YOLO11n object detection model
    trained on a PCB manufacturing defect dataset.

    The model detects defects using bounding boxes and
    provides the detected defect class and confidence score.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "PCB Manufacturing Defect Detection | "
    "YOLO11n Object Detection"
)