from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'received_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Register this function as a route
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # # ✅ Check that it's an image
    # if not file.content_type.startswith('image/'):
    #     return jsonify({'error': 'Uploaded file is not an image'}), 400

    # Save the file
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    return jsonify({'message': f'Image saved as {filename}'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
