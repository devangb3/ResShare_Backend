# ResShare_Backend

This is the backend for the ResShare application.

-Setup the Frontend : "https://github.com/devangb3/ResShare-Frontend"
## Prerequisites

### GCC and G++
- `sudo apt install gcc-11`
- `sudo apt install g++-11`

### C++
- OpenSSL
- libssl-dev

### Python
- Python 3.8

## Installation

1. Install C++ dependencies:

sudo apt install openssl
sudo apt install libssl-dev


2. Install Python dependencies:

pip install -r requirements.txt

## Building the Project

To build the project, navigate to the bazel directory and run:



### For Ubuntu 24
`cd bazel`


`
bazel build //... --action_env=CC=/usr/bin/gcc-11 --action_env=CXX=/usr/bin/g++-11 --cxxopt="-std=c++17"
`

### For Ubuntu 22
`cd bazel`


`bazel build //...`


## Run the Flask Server: Start the Flask server to verify that it is running correctly.

export FLASK_APP=controller.py
flask run
OR 
python3 controller.py
## Testing

1) Upload a file : curl -X POST http://localhost:5000/upload -H "Content-Type: application/json" -d '{"file_path": "/home/...."}'
2) Get All peers : curl -X GET http://localhost:5000/peers
3) Get file stauts: curl -X GET http://localhost:5000/file_status/QmeomffUNfmQy76CQGy9NdmqEnnHU9soCexBnGU3ezPHVH
4) Download a file: curl -X POST http://localhost:5000/download -H "Content-Type: application/json" -d '{"cid": "QmeomffUNfmQy76CQGy9NdmqEnnHU9soCexBnGU3ezPHVH", "file_path": "/home/...."}'
5) Get other peer's file structure : curl -X GET http://localhost:5000/peer_files/12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg
6) Get All files : curl -X GET http://localhost:5000/all_files
7) Delete file : curl -X POST http://localhost:5000/delete -H "Content-Type: application/json" -d '{"cid": "QmeomffUNfmQy76CQGy9NdmqEnnHU9soCexBnGU3ezPHVH"}'
9) Add peer as favorite : curl -X POST "http://127.0.0.1:5000/add_fav_peers" -H "Content-Type: application/json" -d '{"peer_id": "12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU", "nickname": "Bro"}'
10) Get favorite peers :  curl -X GET http://127.0.0.1:5000/fav_peers
11) Edit Favorite Peer Nickame : curl -X PUT "http://127.0.0.1:5000/rename_fav_peers/12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU" -H "Content-Type: application/json" -d '{"new_nickname": "UpdatedNickname"}'
12) Remove Peer : curl -X DELETE "http://127.0.0.1:5000/remove_fav_peers/12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU" -H "Content-Type: application/json"
13) Get Dashboard Data: curl -X GET http://localhost:5000/dashboard/file-stats

