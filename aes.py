import os
import sys
sys.path.append(os.path.abspath("bazel/bazel-bin/aes/"))

import pybind_aes

def encrypt_file(file_path: str, key: str = None):
    if key == None:
        key = pybind_aes.aes_key_generate()
    pybind_aes.aes_file_encrypt(file_path, key)
    return key


def decrypt_file(in_file_path: str, out_file_path: str, key: str):
    return pybind_aes.aes_file_decrypt(in_file_path, out_file_path, key)


