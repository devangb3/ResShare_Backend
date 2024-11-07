package(default_visibility = ["//visibility:public"])
cc_binary(
    name = "pybind_aes.so",
    srcs = ["aes.cpp"],
    linkshared = 1,
    linkstatic = 1,
    linkopts = [
        "-lssl",
        "-lcrypto",
    ],
    deps = [
        "@pybind11//:pybind11",
    ],
)
py_library(
    name = "pybind_aes_so",
    data = [":pybind_aes.so"],
    imports = ["."],
)