import os
import cv2
import base64
import numpy as np
from flask import Flask, render_template_string, request
from ultralytics import YOLO
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Model Loading
model_microplastic = None

def load_model():
    global model_microplastic
    if model_microplastic is None:
        model_path = os.path.join(os.path.dirname(__file__), 'best_microplastic_model.pt')
        if os.path.exists(model_path):
            model_microplastic = YOLO(model_path)
            print("Model Loaded Successfully")
    return model_microplastic

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ============================================================================== 
# HTML Templates (Based on your preferred colors: #005f73, #0a9396, #e9f5f5)
# ==============================================================================

COMMON_STYLE = """
<style>
    body { font-family: sans-serif; background-color: #f0f2f5; margin: 0; padding: 0; text-align: center; }
    .navbar { background-color: #005f73; padding: 15px; color: white; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); display: inline-block; min-width: 500px; margin-top: 20px; }
    h1 { color: #005f73; margin-bottom: 20px; }
    .btn-main { background-color: #0a9396; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-size: 18px; font-weight: 700; border: none; cursor: pointer; transition: 0.3s; display: inline-block; }
    .btn-main:hover { background-color: #005f73; }
    .result-box { background-color: #e9f5f5; border: 2px solid #0a9396; border-radius: 10px; padding: 25px; margin-top: 20px; text-align: left; display: inline-block; width: 100%; box-sizing: border-box; }
    .result-box h2 { margin-top: 0; color: #005f73; border-bottom: 1px solid #0a9396; padding-bottom: 10px; }
    .result-text { font-size: 18px; color: #333; margin: 10px 0; }
    .highlight { font-weight: bold; color: #ae2012; font-size: 22px; }
    img { max-width: 100%; border-radius: 8px; border: 2px solid #0a9396; margin-top: 10px; }
    #drop-area { border: 2px dashed #0a9396; border-radius: 8px; padding: 60px; background-color: #e9f5f5; cursor: pointer; }
</style>
"""

HOME_PAGE = f"""
<!DOCTYPE html><html lang="en"><head><title>Microplastic Dashboard</title>{COMMON_STYLE}</head>
<body>
    <div class="navbar"><h2>🌊 MICROPLASTIC AI ANALYZER</h2></div>
    <div class="container">
        <h1>Detection Dashboard</h1>
        <p>Analyze water samples for microplastic particles instantly.</p>
        <div id="drop-area" onclick="document.getElementById('file-input').click()">
            <form action="/predict" method="post" enctype="multipart/form-data" id="upload-form">
                <input type="file" id="file-input" name="file" accept="image/*" style="display:none" onchange="document.getElementById('upload-form').submit()">
                <span class="btn-main">Start Detection</span>
                <p>Click to choose or drag an image here</p>
            </form>
        </div>
    </div>
</body></html>
"""

RESULT_PAGE = f"""
<!DOCTYPE html><html lang="en"><head><title>Analysis Results</title>{COMMON_STYLE}</head>
<body>
    <div class="navbar"><h2>📊 ANALYSIS REPORT</h2></div>
    <div class="container" style="max-width: 800px;">
        <h1>Detection Result</h1>
        <img src="data:image/jpeg;base64,{{{{img_data}}}}" alt="Result Image">
        
        <div class="result-box">
            <h2>Result Summary</h2>
            <p class="result-text">Status: <strong>Microplastic Found</strong></p>
            <p class="result-text">Total Detections: <span class="highlight">{{{{count}}}}</span></p>
            <p class="result-text">Avg Particle Size: <span class="highlight">{{{{avg_size}}}} px</span></p>
            <p class="result-text">Size Range: <strong>{{{{min_size}}}}px - {{{{max_size}}}}px</strong></p>
        </div>
        
        <br>
        <a href="/" class="btn-main" style="margin-top: 20px;">Upload Another Sample</a>
    </div>
</body></html>
"""

# ============================================================================== 
# Routes Logic
# ==============================================================================

@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/predict', methods=['POST'])
def predict():
    model = load_model()
    if 'file' not in request.files: return "No file", 400
    file = request.files['file']
    if file.filename == '': return "No file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # YOLO Prediction
    results = model.predict(source=filepath, conf=0.25, verbose=False)
    
    # Calculate Counts and Sizes
    detection_count = len(results[0].boxes)
    sizes = []
    for box in results[0].boxes:
        w, h = box.xywh[0][2], box.xywh[0][3]
        sizes.append(round((float(w) + float(h)) / 2, 2))

    avg_s = round(np.mean(sizes), 2) if sizes else 0
    min_s = min(sizes) if sizes else 0
    max_s = max(sizes) if sizes else 0

    # Force Label to "Microplastic"
    for r in results:
        r.names[0] = "Microplastic"

    # Annotated Image
    annotated_image = results[0].plot()
    _, buffer = cv2.imencode('.jpg', annotated_image)
    img_str = base64.b64encode(buffer).decode('utf-8')

    os.remove(filepath)
    
    return render_template_string(RESULT_PAGE, 
                                 img_data=img_str, 
                                 count=detection_count,
                                 avg_size=avg_s,
                                 min_size=min_s,
                                 max_size=max_s)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)