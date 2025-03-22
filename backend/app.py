from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from inference import predict_digit

app = Flask(__name__)
CORS(app)  # Allow frontend requests

UPLOAD_FOLDER = 'temp/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        prediction = predict_digit(file_path)
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
