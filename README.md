# ResShare_Backend

This is the backend for the ResShare application.

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


cd bazel
`
bazel build //aes:pybind_aes_so \
    --action_env=CC=/usr/bin/gcc-11 \
    --action_env=CXX=/usr/bin/g++-11 \
    --cxxopt="-std=c++17"
`

## Run the Flask Server: Start the Flask server to verify that it is running correctly.

export FLASK_APP=app/controller.py
flask run

## Testing

1) Upload a file : curl -X POST http://localhost:5000/upload -H "Content-Type: application/json" -d '{"file_path": "/home/devang/Project/test"}'
2) Get All peers : curl -X GET http://localhost:5000/peers
3) Get file stauts: curl -X GET http://localhost:5000/file_status/QmeomffUNfmQy76CQGy9NdmqEnnHU9soCexBnGU3ezPHVH
4) Download a file: curl -X POST http://localhost:5000/download -H "Content-Type: application/json" -d '{"cid": "QmeomffUNfmQy76CQGy9NdmqEnnHU9soCexBnGU3ezPHVH", "file_path": "/home/devang/Project/jaadu"}'
5) Get other peer's file structure : curl -X GET http://localhost:5000/peer_files/12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg
6) Get All files : curl -X GET http://localhost:5000/all_files
