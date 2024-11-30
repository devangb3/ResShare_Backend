from flask import Flask, jsonify, request
import client
import os
from datetime import datetime
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
    home_dir = os.path.expanduser('~')
    
    downloads_folder = os.path.join(home_dir, 'Downloads')
    
    # saving file along with timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    filename = f"({current_timestamp}) {data.get('filename')}"

    
    file_path = os.path.join(downloads_folder, filename)
    
    os.makedirs(downloads_folder, exist_ok=True)
    result = client.download_file(cid, file_path)
    if result['success']:
        return jsonify({"status": "success", "message": result['message']}), 200
    else:
        return jsonify({"status": "failure", "message": result['message']}), 500

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
    
    return jsonify({"data": all_files}), 200

@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.json
    cid = data.get('cid')
    deletion_status = client.delete_file(cid)
    return jsonify({"status": deletion_status}), 200

@app.route('/fav_peers', methods=['GET'])
def get_favorite_peers():

    try:
        favorite_peers = client.get_my_favorite_peer()
        
        return jsonify({
            "status": "success",
            "data": favorite_peers
        }), 200
    except Exception as e:
        print(f"Error fetching favorite peers: {e}")
        
        return jsonify({
            "status": "error",
            "message": "Failed to fetch favorite peers."
        }), 500

@app.route('/add_fav_peers', methods=['POST'])
def add_favorite_peer_controller():
    try:
        request_data = request.get_json()

        if not request_data:
            return jsonify({
                "status": "error",
                "message": "Invalid input. JSON payload expected."
            }), 400
        
        peer_id = request_data.get('peer_id')
        nickname = request_data.get('nickname')

        if not peer_id or not nickname:
            return jsonify({
                "status": "error",
                "message": "Both 'peer_id' and 'nickname' are required."
            }), 400

        updated_favorite_list = client.add_favorite_peer(peer_id, nickname)

        return jsonify({
            "status": "success",
            "data": updated_favorite_list
        }), 200

    except Exception as e:
        print(f"Error adding favorite peer: {e}")
        
        return jsonify({
            "status": "error",
            "message": "Failed to add favorite peer."
        }), 500

@app.route('/rename_fav_peers/<peer_id>', methods=['PUT'])
def change_nickname_controller(peer_id):

    try:
        request_data = request.get_json()

        if not request_data:
            return jsonify({
                "status": "error",
                "message": "Invalid input. JSON payload expected."
            }), 400
        
        new_nickname = request_data.get('new_nickname')

        if not new_nickname:
            return jsonify({
                "status": "error",
                "message": "The 'new_nickname' field is required."
            }), 400

        updated_favorite_list = client.change_nickname(peer_id, new_nickname)

        return jsonify({
            "status": "success",
            "data": updated_favorite_list
        }), 200

    except KeyError:
        return jsonify({
            "status": "error",
            "message": f"No peer found with ID {peer_id}."
        }), 404
    except Exception as e:
        print(f"Error changing nickname: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to change nickname."
        }), 500

@app.route('/remove_fav_peers/<peer_id>', methods=['DELETE'])
def remove_favorite_peer_controller(peer_id):
    try:
        updated_favorite_list = client.remove_favorite_peer(peer_id)

        if peer_id not in updated_favorite_list:
            return jsonify({
                "status": "success",
                "message": f"Peer {peer_id} successfully removed.",
                "data": updated_favorite_list
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Failed to remove peer {peer_id}. Peer might not exist."
            }), 400

    except Exception as e:
        print(f"Error removing favorite peer: {e}")
        return jsonify({
            "status": "error",
            "message": "Failed to remove favorite peer."
        }), 500


@app.route('/dashboard/file-stats', methods=['GET'])
def get_dashboard_stats():
    dashboard_data = client.fetch_dashboard_data()
    
    return jsonify({"data": dashboard_data}), 200
if __name__ == '__main__':
    app.run(debug=True)
