from flask import Flask, jsonify, request
import client
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.json.get('file_path')
    client.upload_file(file_path)
    return jsonify({"status": "File uploaded successfully"}), 200

@app.route('/download', methods=['POST'])
def download_file():
    data = request.json
    cid = data.get('cid')
    #file_path = data.get('file_path')
        # Get the user's home directory
    home_dir = os.path.expanduser('~')
    
    # Construct the path to the Downloads folder
    downloads_folder = os.path.join(home_dir, 'Downloads')
    
    # Get the filename from the CID or use a default name
    filename = f"{cid}.file"  # You might want to adjust this based on your needs
    
    # Construct the full file path
    file_path = os.path.join(downloads_folder, filename)
    
    # Ensure the Downloads folder exists
    os.makedirs(downloads_folder, exist_ok=True)
    client.download_file(cid, file_path)
    return jsonify({"status": "File downloaded successfully"}), 200

@app.route('/peers', methods=['GET'])
def get_all_peers():
    peers = client.get_all_peers()
    return jsonify(peers), 200

@app.route('/pinned_files', methods=['GET'])
def get_all_pinned_files():
    pinned_files = client.get_all_pinned_file()
    return jsonify(pinned_files), 200

@app.route('/file_status/<string:cid>', methods=['GET'])
def get_file_status(cid):
    file_status = client.get_file_status(cid)
    return jsonify(file_status), 200

@app.route('/peer_files/<string:peer_id>', methods=['GET'])
def get_other_peer_file_structure(peer_id):
    files = client.get_other_peer_file_structure(peer_id)
    return jsonify(files), 200

@app.route('/all_files', methods=['GET'])
def get_all_files():
    all_files = client.get_all_file()
    formatted_files = []
    for peer_id, files in all_files.items():
        if files:  # Only add entries with file data
            for cid, file_info in files.items():
                formatted_files.append({
                    'peerID': peer_id,
                    'fileName': file_info.get('file_name'),
                    'fileSize': file_info.get('file_size'),
                    'CID': cid
                })
    return jsonify({"data": formatted_files}), 200
    #return jsonify(all_files), 200

if __name__ == '__main__':
    app.run(debug=True)
