# ResShare_Backend

This is the backend for the ResShare application.

## Prerequisites

### C++
- OpenSSL
- libssl-dev

### Python
- Python 3.8

## Installation

1. Install C++ dependencies:

sudo apt install openssl
sudo apt install libssl-dev
text

2. Install Python dependencies:

pip install -r requirements.txt
text

## Building the Project

To build the project, navigate to the bazel directory and run:


cd bazel
bazel build //...