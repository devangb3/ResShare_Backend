import requests

ipfs_cluster_api_url = None
ipfs_gateway_url = None


def read_config_file():
    """
    Reads the IPFS Cluster API URL and IPFS Gateway URL from the configuration file.
    Sets the values of global variables ipfs_cluster_api_url and ipfs_gateway_url.
    """
    global ipfs_cluster_api_url, ipfs_gateway_url
    with open("config/ipfs.config") as f:
        ipfs_cluster_api_url = f.readline().strip()
        ipfs_gateway_url = f.readline().strip()


def add_file_to_cluster(file_path):
    """
    Adds a file to the IPFS Cluster.

    :param file_path: The path to the file to be added.
    :return: The CID (Content Identifier) of the file if successful, otherwise None.
    """
    if ipfs_cluster_api_url is None or ipfs_gateway_url is None:
        read_config_file()

    url = ipfs_cluster_api_url + "add"
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        cid = response.json()['cid']['/']
        print(f"File added successfully with CID: {cid}")
        return cid
    else:
        print("Failed to add file to IPFS Cluster.")
        print(response.text)


def pin_file(cid, replication_min, replication_max):
    """
    Pins a file in the IPFS Cluster to ensure it remains available.

    :param cid: The CID of the file to be pinned.
    :param replication_min: The minimum number of replicas.
    :param replication_max: The maximum number of replicas.
    """
    if ipfs_cluster_api_url is None or ipfs_gateway_url is None:
        read_config_file()

    url = f"{ipfs_cluster_api_url}pins/{cid}"
    payload = {
        "replication-min": replication_min,
        "replication-max": replication_max
    }
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"File with CID {cid} pinned successfully.")
    else:
        print("Failed to pin file to IPFS Cluster.")
        print(response.text)


def get_file_status(cid):
    """
    Retrieves the status of a file in the IPFS Cluster.

    :param cid: The CID of the file.
    :return: The status information of the file if successful, otherwise None.
    """
    if ipfs_cluster_api_url is None or ipfs_gateway_url is None:
        read_config_file()

    url = f"{ipfs_cluster_api_url}pins/{cid}"
    response = requests.get(url)

    if response.status_code == 200:
        file_info = response.json()
        print(f"File status: {file_info}")
        return file_info
    else:
        print("Failed to get file status from IPFS Cluster.")
        print(response.text)


def download_file_from_ipfs(cid, save_path):
    if ipfs_cluster_api_url is None or ipfs_gateway_url is None:
        read_config_file()

    # Print the configuration to verify
    print(f"IPFS Cluster API URL: {ipfs_cluster_api_url}")
    print(f"IPFS Gateway URL: {ipfs_gateway_url}")

    url = f"{ipfs_gateway_url}ipfs/{cid}"
    print(f"Download URL: {url}")

    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"File downloaded successfully and saved to {save_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from IPFS: {e}")


def list_pinned_files():
    """
    Retrieves information about all pinned files in the IPFS Cluster.

    :return: A list of information about pinned files if successful, otherwise None.
    """
    if ipfs_cluster_api_url is None or ipfs_gateway_url is None:
        read_config_file()

    url = f"{ipfs_cluster_api_url}pins"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pinned_files = response.json()
            for info in pinned_files:
                print(f"{info}")
            return pinned_files[0]
        else:
            print(f"Failed to retrieve pinned files. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to IPFS Cluster API: {e}")


def list_all_peers():
    """
    Retrieves information about all peers in the IPFS Cluster.

    :return: A list of information about all peers if successful, otherwise None.
    """
    if ipfs_cluster_api_url is None or ipfs_gateway_url is None:
        read_config_file()

    url = f"{ipfs_cluster_api_url}/peers"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            peers_info = response.json()
            print("Current Peers in IPFS Cluster:")
            for peer in peers_info:
                peer_id = peer.get('id', 'Unknown ID')
                addresses = peer.get('addresses', [])
                print(f"Peer ID: {peer_id}")
                print("Addresses:")
                for address in addresses:
                    print(f"  - {address}")
            return peers_info[0]
        else:
            print(f"Failed to retrieve peers info. Status code: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to IPFS Cluster API: {e}")


# cid = add_file_to_cluster("test.txt")
# print(cid)

# pin_file("QmVGp7rNegQrd86YNViYzuLMBYPHiqE3usij9AuZAJzdSn", 1, 10)

# get_file_status("QmVGp7rNegQrd86YNViYzuLMBYPHiqE3usij9AuZAJzdSn")

# download_file_from_ipfs("QmVGp7rNegQrd86YNViYzuLMBYPHiqE3usij9AuZAJzdSn", "test2.txt")

# list_pinned_files()
res = list_all_peers()
print(res)
