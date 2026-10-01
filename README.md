# 🔍 PCB Defect Detection Using YOLO

An AI-powered computer vision application for detecting and localizing defects in Printed Circuit Boards (PCBs) using **YOLO (You Only Look Once)**. The trained model identifies defects in PCB images and displays bounding boxes, defect classes, and confidence scores through an interactive **Streamlit** web application.

## 🚀 Project Overview

In PCB manufacturing, detecting defects accurately and quickly is important for maintaining product quality.

This project uses a YOLO object detection model to automatically identify PCB defects from images.

The application allows users to:

* Upload a PCB image
* Select sample PCB images
* Detect defects using the trained YOLO model
* View bounding boxes around detected defects
* View the detected defect class
* View confidence scores
* Analyze multiple defects in a single image

## 🧠 Technologies Used

* **Python**
* **YOLO / Ultralytics**
* **Computer Vision**
* **OpenCV**
* **Pillow**
* **NumPy**
* **Streamlit**

## 🏗️ Project Architecture

```text
PCB Image
    ↓
Streamlit Web Application
    ↓
YOLO Object Detection Model
    ↓
Defect Detection
    ↓
Bounding Boxes + Class + Confidence
    ↓
Visualized Result
```

## 📂 Project Structure

```text
manufacture_defective/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   └── best.pt
│
└── sample_images/
    ├── pcb1.jpg
    ├── pcb2.jpg
    ├── pcb3.jpg
    └── pcb4.jpg
```

## 📊 Dataset

The model was trained on a PCB defect detection dataset containing PCB images and corresponding object-detection annotations.

The dataset contains multiple defect categories represented using YOLO-format annotations.

The training and validation datasets are kept separately from the deployment repository to keep the GitHub project lightweight.

## 🎯 Model

The project uses a **YOLO object detection model** trained specifically for PCB defect detection.

The trained model is stored as:

```text
models/best.pt
```

The model performs object detection rather than simple image classification, allowing the application to identify **where** a defect occurs in the PCB image.

## 🖥️ Streamlit Application

The application provides an interactive interface where users can:

1. Upload a PCB image.
2. Select a sample image.
3. Run YOLO inference.
4. View detected defects.
5. Inspect bounding boxes and confidence scores.

### Example

```text
Input PCB Image
       ↓
YOLO Inference
       ↓
Detected Defect
       ↓
Bounding Box + Confidence
```

## 📸 Application Screenshots

### Input

*Add screenshot of the Streamlit application here.*

### Detection Result

*Add screenshot showing the PCB image with YOLO bounding boxes here.*

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd manufacture_defective
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser.

## 🌐 Deployment

The application is deployed using **Streamlit Community Cloud**.

**Live Demo:**
*Add your deployed Streamlit URL here.*

## 📈 Results

The trained YOLO model can detect PCB defects and localize them using bounding boxes.

The application displays:

* Defect class
* Detection confidence
* Location of detected defects
* Annotated PCB image

*Model performance metrics and sample results can be added here after final evaluation.*

## 🔮 Future Improvements

* Improve detection accuracy with additional training data
* Increase the number of PCB defect categories
* Add real-time camera/video inspection
* Add production-line integration
* Add defect statistics and analytics dashboard
* Optimize the model for edge/industrial deployment

## 👩‍💻 Author

**Alekhya**

B.Tech — Computer Science / AI & ML

Interested in **AI Engineering, Machine Learning and Computer Vision**.

## ⭐ Acknowledgements

* Ultralytics YOLO
* Streamlit
* OpenCV
* PCB defect detection dataset used for model training
