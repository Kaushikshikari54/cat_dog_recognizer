import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import your corrected prediction logic
from predictor import predict_image 

app = Flask(__name__)

# 1. Security & Config
# CORS allows your frontend (port 8000) to talk to this backend (port 5000)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB Limit

# 2. Path Handling
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 3. Validation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return "Cat-Dog Classifier API Running 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "File type not supported."}), 400

        # 4. Save the file securely
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # 5. Inference
        label, confidence = predict_image(file_path)

        # 6. Confidence Threshold
        threshold = 0.70
        final_label = str(label)
        
        if confidence < threshold:
            final_label = "Unknown/Uncertain"

        return jsonify({
            "prediction": final_label,
            "confidence": round(float(confidence), 4),
            "status": "success"
        })

    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Runs on http://127.0.0.1:5000
    app.run(debug=True, port=5000)