from flask import Flask, jsonify, request
import client

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.json.get('file_path')
    client.upload_file(file_path)
    return jsonify({"status": "File uploaded successfully"}), 200

@app.route('/download', methods=['POST'])
def download_file():
    data = request.json
    cid = data.get('cid')
    file_path = data.get('file_path')
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
    return jsonify(all_files), 200

if __name__ == '__main__':
    app.run(debug=True)
