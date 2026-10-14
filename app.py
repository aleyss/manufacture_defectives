import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import datetime
import os
from copilot_engine import generate_8d_analysis, answer_technician_question
from knowledge_base import PCB_DEFECT_KB

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="PCB AOI Defect Inspection Copilot",
    page_icon="🏭",
    layout="wide"
)

# Custom Styling for Industrial Theme
st.markdown("""
    <style>
    .metric-card {
        background-color: #0e1117;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00c0f2;
    }
    .stAlert {
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(BASE_DIR, "weights", "best.pt")

@st.cache_resource
def load_yolo():
    return YOLO(MODEL_PATH)

try:
    model = load_yolo()
    class_names = model.names
except Exception as e:
    st.error(f"Error loading model from {MODEL_PATH}: {e}")
    st.stop()

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
with st.sidebar:
    st.title("🏭 AOI Control Station")
    st.caption("Automated Optical Inspection + GenAI Copilot")
    st.divider()

    st.subheader("⚙️ Inspection Settings")
    conf_threshold = st.slider("Detection Confidence Threshold", 0.05, 0.90, 0.15, 0.05)
    ipc_class_target = st.selectbox(
        "Target Quality Standard",
        [
            "IPC-A-610 Class 2 (Dedicated Service)",
            "IPC-A-610 Class 3 (High Reliability)",
            "IPC-A-610 Class 1 (General Consumer)"
        ]
    )
    
    st.divider()
    st.subheader("🧠 SLM Copilot Engine")
    slm_backend = st.selectbox(
        "Reasoning Engine",
        [
            "Industrial Rule Synthesizer (Zero-Latency Fallback)",
            "Local Ollama (Llama-3.2 / Qwen-2.5)"
        ]
    )
    backend_key = "local_ollama" if "Ollama" in slm_backend else "fallback"

    st.divider()
    st.subheader("📋 Active Defect Classes (6-Class)")
    st.markdown("\n".join([f"- **ID {k}:** `{v}`" for k, v in class_names.items()]))

# ============================================================
# MAIN HEADER
# ============================================================
st.title("🛡️ PCB Defect Inspection & 8D Root-Cause Copilot")
st.markdown("Combines **YOLO11n Real-time Object Detection** (6 Defect Classes) with **Autonomous SLM Reasoning** grounded on **IPC-A-610** manufacturing standards.")

st.divider()

# ============================================================
# IMAGE SELECTION & UPLOAD
# ============================================================
col_up1, col_up2 = st.columns([1.5, 1.5])

SAMPLE_MAP = {
    "None": None,
    "Spur Defect (test_folder)": os.path.join(BASE_DIR, "test_folder", "l_light_04_spur_15_1_600.jpg"),
    "Spurious Copper Defect (test_folder)": os.path.join(BASE_DIR, "test_folder", "l_light_04_spurious_copper_02_3_600.jpg"),
    "Mouse Bite Defect (test_folder)": os.path.join(BASE_DIR, "test_folder", "l_light_06_mouse_bite_07_3_600.jpg"),
    "Open Circuit Defect (test_folder)": os.path.join(BASE_DIR, "test_folder", "l_light_10_open_circuit_04_2_600.jpg"),
    "Short Circuit Defect (test_folder)": os.path.join(BASE_DIR, "test_folder", "l_light_06_short_05_1_600.jpg"),
    "Sample Board 1 (sample_images/pcb1.jpg)": os.path.join(BASE_DIR, "sample_images", "pcb1.jpg"),
    "Sample Board 2 (sample_images/pcb3.jpg)": os.path.join(BASE_DIR, "sample_images", "pcb3.jpg"),
    "Sample Board 3 (sample_images/pcb4.jpg)": os.path.join(BASE_DIR, "sample_images", "pcb4.jpg")
}

with col_up1:
    uploaded_file = st.file_uploader("📷 Ingest High-Resolution PCB Inspection Image", type=["jpg", "jpeg", "png"])

with col_up2:
    st.write("**Or select from pre-loaded verification boards:**")
    sample_choice = st.selectbox("Select Sample Defect PCB", list(SAMPLE_MAP.keys()))

# Load image logic
image = None
image_source_label = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_source_label = uploaded_file.name
elif sample_choice != "None" and SAMPLE_MAP[sample_choice]:
    sample_path = SAMPLE_MAP[sample_choice]
    if os.path.exists(sample_path):
        image = Image.open(sample_path).convert("RGB")
        image_source_label = os.path.basename(sample_path)
    else:
        st.warning(f"File not found at `{sample_path}`. Please upload an image.")

# ============================================================
# PROCESSING PIPELINE
# ============================================================
if image is not None:
    # 1. RUN YOLO INFERENCE
    with st.spinner("Executing YOLO11n 6-Class Defect Inference..."):
        results = model.predict(source=image, imgsz=640, conf=conf_threshold, verbose=False)
        result = results[0]

    # Visual layout: 2 Columns
    col_vis1, col_vis2 = st.columns(2)

    with col_vis1:
        st.subheader("📸 Inspection View (Raw)")
        st.image(image, caption=f"Source: {image_source_label}", use_container_width=True)

    with col_vis2:
        st.subheader("🎯 AOI Vision Overlay")
        annotated_image = result.plot()[:, :, ::-1] # BGR to RGB
        st.image(annotated_image, caption=f"Detections with conf >= {conf_threshold:.2f}", use_container_width=True)

    st.divider()

    # 2. CHECK DETECTIONS
    if result.boxes is not None and len(result.boxes) > 0:
        boxes_data = result.boxes
        num_defects = len(boxes_data)
        
        # Summary KPI Ribbon
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Total Defects Flagged", num_defects)
        highest_conf = float(boxes_data.conf.max().cpu().numpy()) * 100
        kpi2.metric("Peak Confidence", f"{highest_conf:.1f}%")
        kpi3.metric("Standard Applied", ipc_class_target.split()[0])
        kpi4.metric("Status", "⚠️ ACTION REQUIRED", delta="-Defect Detected", delta_color="inverse")

        st.subheader("🔍 Defect Breakdown & Region of Interest (ROI)")
        
        defect_tabs = st.tabs([f"Defect #{i+1}: {class_names[int(boxes_data.cls[i])]}" for i in range(num_defects)])

        # Store primary defect for report
        primary_defect_info = None

        for i, tab in enumerate(defect_tabs):
            with tab:
                c_id = int(boxes_data.cls[i].cpu().numpy())
                c_name = class_names[c_id]
                conf = float(boxes_data.conf[i].cpu().numpy())
                xyxy = boxes_data.xyxy[i].cpu().numpy().astype(int)

                if i == 0:
                    primary_defect_info = (c_name, conf, xyxy.tolist())

                tab_col1, tab_col2 = st.columns([1, 2])

                # Crop ROI
                with tab_col1:
                    w, h = image.size
                    pad = 15
                    x1, y1 = max(0, xyxy[0] - pad), max(0, xyxy[1] - pad)
                    x2, y2 = min(w, xyxy[2] + pad), min(h, xyxy[3] + pad)
                    cropped_roi = image.crop((x1, y1, x2, y2))
                    
                    st.write("**Cropped Defect (Magnified):**")
                    st.image(cropped_roi, caption=f"ROI: ({xyxy[0]}, {xyxy[1]}) to ({xyxy[2]}, {xyxy[3]})", width=220)
                    st.metric("Defect Class", f"{c_name} (ID: {c_id})")
                    st.metric("Confidence Score", f"{conf * 100:.2f}%")

                # Autonomous SLM Engineering Assessment
                with tab_col2:
                    st.markdown("#### 🧠 Autonomous Copilot 8D Assessment")
                    with st.spinner("Grounding defect against IPC-A-610 standards..."):
                        analysis = generate_8d_analysis(
                            defect_class=c_name,
                            confidence=conf,
                            bbox=xyxy.tolist(),
                            model_backend=backend_key
                        )
                    st.markdown(analysis)

        # ====================================================
        # INTERACTIVE TECHNICIAN CHAT ASSISTANT
        # ====================================================
        st.divider()
        st.subheader("💬 Ask the PCB Quality Copilot")
        st.caption("Line operators and technicians can query rework steps, soldering temperatures, or IPC exceptions in real-time.")

        tech_query = st.text_input(
            "Enter technician query (e.g. 'Can I mechanically scrape this spur?' or 'Is rework permissible for Class 3?')",
            key="chat_input"
        )
        if tech_query and primary_defect_info:
            with st.chat_message("assistant"):
                answer = answer_technician_question(
                    tech_query,
                    primary_defect_info[0],
                    model_backend=backend_key
                )
                st.markdown(answer)

        # ====================================================
        # 1-CLICK 8D QUALITY REPORT EXPORT
        # ====================================================
        st.divider()
        st.subheader("📄 Generate Engineering 8D Incident Report")
        
        report_content = f"""# ====================================================
# OFFICIAL 8D DEFECT & CONTAINMENT INCIDENT REPORT
# ====================================================
Inspection Timestamp: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Facility Station: SMT Assembly Line 02 (AOI Cell)
Board Source: {image_source_label}
Standard Applied: {ipc_class_target}

[DETECTION SUMMARY]
Total Defects Identified: {num_defects}
Primary Defect: {primary_defect_info[0]}
Detection Confidence: {primary_defect_info[1] * 100:.2f}%
Bounding Coordinates: {primary_defect_info[2]}

[ROOT CAUSE & ENGINEERING DIAGNOSIS]
{analysis}

[SIGN-OFF]
Quality Assurance: PCB AI Copilot System
Inspection Status: QUARANTINE / REWORK PENDING
# ====================================================
"""
        st.download_button(
            label="📥 Download Official 8D Quality Report (.txt)",
            data=report_content,
            file_name=f"8D_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    else:
        st.success("✅ **Inspection Passed:** No surface defects detected above confidence threshold. Board conforms to IPC-A-610 standards.")

# ============================================================
# FOOTER & ARCHITECTURE DOCUMENTATION
# ============================================================
st.divider()
with st.expander("📌 System Architecture & Industry Value Details"):
    st.markdown("""
    * **Perception Layer:** YOLO11n object detector localized onto 6 PCB micro-defect classes:
      - `0: mouse_bite`
      - `1: spur`
      - `2: missing_hole`
      - `3: short`
      - `4: open_circuit`
      - `5: spurious_copper`
    * **Domain Knowledge Layer:** Direct lookup into IPC-A-610 electronic assembly acceptability matrices.
    * **Reasoning Copilot:** Local SLM / Industrial Rule Engine generates immediate containment actions and 8D root-cause reports.
    * **Edge Viability:** Fully functional on-premise without requiring cloud API connections.
    """)