from flask import Flask, request, jsonify, send_from_directory
import boto3
import os
from botocore.exceptions import ClientError
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

# S3 Configuration
S3_BUCKET = "hellobucket-clone"  # ✅ Use your actual bucket name
REGION = "us-east-1"

s3 = boto3.client("s3", region_name=REGION)

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
return jsonify({'error': 'No file selected'}), 400
    try:
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
        print(f"Uploaded: {file.filename}")  # DEBUG
        return jsonify({'message': 'File uploaded successfully'}), 200
    except ClientError as e:
        print("Upload error:", e)
        return jsonify({'error': str(e)}), 500


@app.route('/files', methods=['GET'])
def list_files():
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET)  # ✅ Fix: variable name was wrong
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        s3.delete_object(Bucket=S3_BUCKET, Key=filename)
        return jsonify({'message': f'{filename} deleted successfully'}), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
