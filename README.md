# Microplastic Detection & Quantification System 🌊🔬

## Project Overview
This project is an inter-disciplinary collaboration with the **Civil Engineering Department** aimed at automating the detection and analysis of microplastics in water samples. Using **YOLOv8**, the system identifies microplastics, provides spatial localization, and enables quantification for environmental research.

## Key Features
- **Object Detection:** Precise localization of microplastic particles in aquatic samples.
- **Particle Quantification:** Automatic counting and size estimation of detected particles.
- **Statistical Output:** Calculates the average size and distribution across multiple images.
- **Efficiency:** Replaces manual counting methods, significantly reducing analysis time for researchers.

## 🛠️ Technical Stack
- **Model Architecture:** YOLOv8 (Optimized for small object detection)
- **Language:** Python
- **Libraries:** Ultralytics, OpenCV, NumPy, Matplotlib

## 📊 Methodology & Results
The system follows a standard AI pipeline: Pre-processing water sample imagery, performing high-precision inference, and post-processing for size estimation.


![Methodology](docs/methodology.png)


![Results](docs/results_image.jpg)

## 📂 Repository Contents
- `app.py`: Main script for model inference and analysis.
- `uploads/`: Directory containing sample test images.
- `best_microplastic_model.pt`: Pre-trained YOLOv8 weights (optimized for microplastics).
- `docs/`: Technical diagrams and performance reports.

## 📥 Download Trained Model
Due to GitHub's file size restrictions, the trained YOLOv8 model weights are hosted on Google Drive:
- **[Download best_microplastic_model.pt](https://drive.google.com/file/d/1U_koZITZ2jBvrU8yZ-4GJ8o_mXsu38Us/view?usp=sharing)**

*Note: Place this file in the root directory or update the path in `app.py` to run the system.*
---
**Developed by Umar Ayoub**
*Final Year Computer Science (AI) - UET Mardan*
