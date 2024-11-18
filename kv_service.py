import os
import sys
sys.path.append(os.path.abspath("bazel/bazel-bin/kv_service/"))
import pybind_kv
os.path.abspath("config/kv_server.config")
config_path = "config/kv_server.config"

def set_kv(key: str, value: str):
    global config_path
    print(f"SETTING {key}, {value}")
    pybind_kv.set(key, value, config_path)


def get_kv(key: str) -> str:
    global config_path
    print(f"GETTING {key}")
    return pybind_kv.get(key, config_path)

