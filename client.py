import kv_service as kv
import ipfs_cluster as ipfs
import json
import os

# Global variable
my_ipfs_cluster_id = ipfs.get_my_peer_id()

def upload_file(file_path: str):
    """
    The whole process of uploading a file
    This function should be called when user want to upload a file
    my_file_structure:  {
                            CID1(str):  {
                                            "file_name": FILE_NAME_1(str),
                                            "file_size": FILE_SIZE_1(int)(bytes),
                                        },
                            CID2(str):  {
                                            "file_name": FILE_NAME_2(str),
                                            "file_size": FILE_SIZE_2(int)(bytes),
                                        },
                        }


    :param file_path: THe file path on user's local machine
    :return None
    """
    global my_ipfs_cluster_id

    # Get my current files under my IPFS cluster peer ID
    my_file_structure = kv.get_kv(my_ipfs_cluster_id)
    try:
        my_file_structure = json.loads(my_file_structure)
    except:
        print("File structure broken or empty")
        my_file_structure = {}

    # Generate metadata of this file
    new_file_info = {'file_name': os.path.basename(file_path), 'file_size': os.path.getsize(file_path)}

    # Send to IPFS cluster and get CID
    cid = ipfs.add_file_to_cluster(file_path)

    # Update ResilientDB
    my_file_structure[cid] = new_file_info
    kv.set_kv(my_ipfs_cluster_id, json.dumps(my_file_structure))

    #Seperate KV pair for Delete File
    
    delete_file_structure = kv.get_kv(cid)
    try:
        parsed = json.loads(delete_file_structure)
        
        result = {}
        for outer_key, inner_dict in parsed.items():
            result[outer_key] = {}
            for inner_key, value in inner_dict.items():
                result[outer_key][inner_key] = value
        
        delete_file_structure = result
    except json.JSONDecodeError:
        print("Delete File structure is not valid JSON")
        delete_file_structure = {}
    except Exception as e:
        print(f"An error occurred: {e}")
        delete_file_structure = {}

    # Now delete_file_structure has the desired format
    print(delete_file_structure)

    if cid not in delete_file_structure:
        delete_file_structure[cid] = {my_ipfs_cluster_id: False}
    else:
        delete_file_structure[cid][my_ipfs_cluster_id] = False
    
    kv.set_kv(cid, json.dumps(delete_file_structure))

def download_file(cid: str, file_path: str):
    """
    This function will download file with cid to file_path
    :param cid: The file CID that user wants to download
    :param file_path: The file path where user wants to save the file(include file name suche like test.txt)
    """
    return ipfs.download_file_from_ipfs(cid, file_path)


def get_all_peers():
    """
    This function will return all peers that currently on in my ipfs cluster

    :return a python dict
    :return format: {
                        'id': '12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg',
                        'addresses': [
                                        '/ip4/192.168.1.126/tcp/9096/p2p/12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg',
                                        '/ip4/127.0.0.1/tcp/9096/p2p/12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg'
                                    ],
                        'cluster_peers': [
                                            '12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg',
                                            '12D3KooWEhnfrehv1ot3SmFfoQuNFrYi275BHi3eBBQ7CVHFQnMD',
                                            '12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU'
                                        ],
                        'cluster_peers_addresses': [
                                                        '/ip4/127.0.0.1/tcp/9096/p2p/12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU',
                                                        '/ip4/192.168.1.128/tcp/9096/p2p/12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU',
                                                        '/ip4/127.0.0.1/tcp/9096/p2p/12D3KooWEhnfrehv1ot3SmFfoQuNFrYi275BHi3eBBQ7CVHFQnMD',
                                                        '/ip4/192.168.1.127/tcp/9096/p2p/12D3KooWEhnfrehv1ot3SmFfoQuNFrYi275BHi3eBBQ7CVHFQnMD'
                                                    ],
                        'version': '0.14.0',
                        'commit': '',
                        'rpc_protocol_version': '/ipfscluster/0.12/rpc',
                        'error': '',
                        'ipfs': {
                                    'id': '12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz',
                                    'addresses': [
                                                    '/ip4/127.0.0.1/tcp/4001/p2p/12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz',
                                                    '/ip4/127.0.0.1/udp/4001/quic/p2p/12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz',
                                                    '/ip4/192.168.1.126/tcp/4001/p2p/12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz',
                                                    '/ip4/192.168.1.126/udp/4001/quic/p2p/12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz',
                                                    '/ip4/95.179.234.3/udp/4001/quic/p2p/12D3KooWL6m6yiiEzY7iyuxuzbE268cpLsa8g9B5xqwjw1QcbeYj/p2p-circuit/p2p/12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz',
                                                    '/ip6/::1/tcp/4001/p2p/12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz',
                                                    '/ip6/::1/udp/4001/quic/p2p/12D3KooWPXvRC4hgCUBqYSGTMYLCmL7CMP8Xr9dFa2DM5Fnzk8pz'
                                                ],
                                    'error': ''},
                        'peername': 'cluster1'
                    }
    """
    return ipfs.list_all_peers()


def get_all_pinned_file():
    """
    This will return all pinned file info in the cluster

    :return python array
    :return format: [
                        {
                            'cid': {'/': 'QmVGp7rNegQrd86YNViYzuLMBYPHiqE3usij9AuZAJzdSn'},
                            'name': '',
                            'peer_map': {
                                            '12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg': {
                                                                                                        'peername': 'cluster1',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.817110362Z',
                                                                                                        'error': ''
                                                                                                    },
                                            '12D3KooWEhnfrehv1ot3SmFfoQuNFrYi275BHi3eBBQ7CVHFQnMD': {
                                                                                                        'peername': 'cluster2',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.818075701Z',
                                                                                                        'error': ''
                                                                                                    },
                                            '12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU': {
                                                                                                        'peername': 'cluster3',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.815509853Z',
                                                                                                        'error': ''
                                                                                                    }
                                        }
                        },
                        {
                            'cid': {'/': 'QmVd9hKho2C7MHNG21ufLRtE6TsUTHsqmwhwHbtTbfLBbN'},
                            'name': '',
                            'peer_map': {
                                            '12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg': {
                                                                                                        'peername': 'cluster1',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.81711184Z',
                                                                                                        'error': ''
                                                                                                    },
                                            '12D3KooWEhnfrehv1ot3SmFfoQuNFrYi275BHi3eBBQ7CVHFQnMD': {
                                                                                                        'peername': 'cluster2',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.818076878Z',
                                                                                                        'error': ''
                                                                                                    },
                                            '12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU': {
                                                                                                        'peername': 'cluster3',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.815511566Z',
                                                                                                        'error': ''
                                                                                                    }
                                        }
                        },
                        {
                            'cid': {'/': 'QmTZiTzfVqEoUFzMeWE3YHhhVbCVAqFivbBNkkP44GW5H2'},
                            'name': '',
                            'peer_map': {
                                            '12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg': {
                                                                                                        'peername': 'cluster1',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.817107063Z',
                                                                                                        'error': ''
                                                                                                    },
                                            '12D3KooWEhnfrehv1ot3SmFfoQuNFrYi275BHi3eBBQ7CVHFQnMD': {
                                                                                                        'peername': 'cluster2',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.818072068Z',
                                                                                                        'error': ''
                                                                                                    },
                                            '12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU': {
                                                                                                        'peername': 'cluster3',
                                                                                                        'status': 'pinned',
                                                                                                        'timestamp': '2024-11-08T03:34:42.815506422Z',
                                                                                                        'error': ''
                                                                                                    }
                                        }
                        }
                    ]
    """
    return ipfs.list_pinned_files()


def get_file_status(cid: str):
    """
    This function will return file info of a certain file

    :param cid: File CID the user wants to lookup
    :return a python dict
    :return format: {
                        'cid': {'/': 'QmVGp7rNegQrd86YNViYzuLMBYPHiqE3usij9AuZAJzdSn'},
                        'name': '',
                        'peer_map': {
                                        '12D3KooWEH7HALhJhEHY6RQ1SDrxcbrihM8VBy9vB7Rf6GqRFtSg': {
                                                                                                    'peername': 'cluster1',
                                                                                                    'status': 'pinned',
                                                                                                    'timestamp': '2024-11-08T03:42:57.832717171Z',
                                                                                                    'error': ''
                                                                                                },
                                        '12D3KooWEhnfrehv1ot3SmFfoQuNFrYi275BHi3eBBQ7CVHFQnMD': {
                                                                                                    'peername': 'cluster2',
                                                                                                    'status': 'pinned',
                                                                                                    'timestamp': '2024-11-08T03:42:57.83347969Z',
                                                                                                    'error': ''
                                                                                                },
                                        '12D3KooWHYr7SoHVDLHHbvKu8SzwXXTvZ7UqY3Z4D5iXfcPDzEDU': {
                                                                                                    'peername': 'cluster3',
                                                                                                    'status': 'pinned',
                                                                                                    'timestamp': '2024-11-08T03:42:57.830898772Z',
                                                                                                    'error': ''
                                                                                                }
                                    }
                    }
    """
    return ipfs.get_file_status(cid)


def get_other_peer_file_structure(peer_id: str):
    """
    This function will return all files that belows to a certain peer
    :param peer_id: The peer ID that user wants to lookup
    :return A python dict
    :return format: Same as my_file_structure in upload_file(). If return an empty dict {} means this user hasn't upload
                    any files yet
    """
    peer_file_structure = kv.get_kv(peer_id)
    try:
        peer_file_structure = json.loads(peer_file_structure)
    except:
        peer_file_structure = {}
    return peer_file_structure


def get_all_file():
    """
    This function will return all file info that current cluster has

    :return a python dict
    :return format: {
                        PEER_ID_1(str): {
                                            CID1(str):  {
                                                            "file_name": FILE_NAME_1(str),
                                                            "file_size": FILE_SIZE_1(int)(bytes),
                                                        },
                                            CID2(str):  {
                                                            "file_name": FILE_NAME_2(str),
                                                            "file_size": FILE_SIZE_2(int)(bytes),
                                                        },
                                        }，
                        PEER_ID_2(str): {},
                    }
    """
    peers = get_all_peers()["cluster_peers"]
    res = {}
    for peer in peers:
        res[peer] = get_other_peer_file_structure(peer)
    return res


def add_favorite_peer(peer_id: str, nickname: str) -> dict:
    """
    This function allows user to add their favorite peers, make sure that user can find the file faster
    :param peer_id: The peer id that user wan to add
    :param nickname: The nickname user wants to assign to this peer id.

    :return a python dict of the modification
    :return format  {
                        PEER_ID_1(str): {
                                            'nickname': NICKNAME_1(str),
                                            'peer_name': PEER_NAME_1(str)(Peer name is the PEER_ID's corresponding name)
                                        },
                        PEER_ID_2(str): {
                                            'nickname': NICKNAME_2(str),
                                            'peer_name': PEER_NAME_2(str)(Peer name is the PEER_ID's corresponding name)
                                        },
                    }
    """
    my_favorite_list = kv.get_kv(my_ipfs_cluster_id + " FAVORITE")
    peer_name = ipfs.get_peer_name(peer_id)
    try:
        my_favorite_list = json.loads(my_favorite_list)
    except:
        print("Your favorite peer list is currently empty or broken, creating a new one.")
        my_favorite_list = {}

    my_favorite_list[peer_id] = {'nickname': nickname, 'peer_name': peer_name}

    kv.set_kv(my_ipfs_cluster_id + " FAVORITE", json.dumps(my_favorite_list))
    return my_favorite_list


def change_nickname(peer_id: str, new_nickname: str) -> dict:
    """
    This function allows user to change the peer name of their favorite peers

    :param peer_id: The target peer id that user want to change the nickname
    :param new_nickname: The new nickname user want to assign

    :return a python dict after modification
    :return format: Please follow add_favorite_peer() return format
    """

    my_favorite_list = kv.get_kv(my_ipfs_cluster_id + " FAVORITE")
    try:
        my_favorite_list = json.loads(my_favorite_list)
    except:
        print("Your favorite peer list is currently empty or broken, creating a new one.")
        return {}

    my_favorite_list[peer_id]['nickname'] = new_nickname
    kv.set_kv(my_ipfs_cluster_id + " FAVORITE", json.dumps(my_favorite_list))

    return my_favorite_list


def remove_favorite_peer(peer_id) -> dict:
    """
    This function allows user to delete one of their favorite peers

    :param peer_id: The target peer id that user want to delete

    :return a python dict after modification
    :return format: Please follow add_favorite_peer() return format
    """
    my_favorite_list = kv.get_kv(my_ipfs_cluster_id + " FAVORITE")
    try:
        my_favorite_list = json.loads(my_favorite_list)
    except:
        print("Your favorite peer list is currently empty or broken, creating a new one.")
        return {}

    try:
        del my_favorite_list[peer_id]
        kv.set_kv(my_ipfs_cluster_id + " FAVORITE", json.dumps(my_favorite_list))
        return my_favorite_list
    except:
        print(f"{peer_id} not found.")
        return my_favorite_list


def get_my_favorite_peer() -> dict:
    """
    This function will get all favorite peers
    This function should be called only once at initial loading

    :return a python dict after modification
    :return format: Please follow add_favorite_peer() return format
    """
    my_favorite_list = kv.get_kv(my_ipfs_cluster_id + " FAVORITE")
    try:
        my_favorite_list = json.loads(my_favorite_list)
        return my_favorite_list
    except:
        print("Your favorite peer list is currently empty or broken, creating a new one.")
        return {}

def delete_file(cid:str) -> bool:
    global my_ipfs_cluster_id
    delete_file_structure = kv.get_kv(cid)
    try:
        parsed = json.loads(delete_file_structure)
        
        result = {}
        for outer_key, inner_dict in parsed.items():
            result[outer_key] = {}
            for inner_key, value in inner_dict.items():
                result[outer_key][inner_key] = value
        
        delete_file_structure = result
    except json.JSONDecodeError:
        print("Delete File structure is not valid JSON")
        delete_file_structure = {}
    except Exception as e:
        print(f"An error occurred: {e}")
        delete_file_structure = {}


    if cid not in delete_file_structure:
        print(f"File with CID {cid} not found")
        return False
    
    if my_ipfs_cluster_id not in delete_file_structure[cid]:
        print(f"Peer {my_ipfs_cluster_id} does not have access to this file for deletion")
        return False
    delete_file_structure[cid][my_ipfs_cluster_id] = True
    try:
        kv.set_kv(cid, json.dumps(delete_file_structure))
    except Exception as e:
        print(f"Error updating ResilientDB: {str(e)}")
        return False
    peer_values = delete_file_structure[cid]
    
    all_peers_true = all(value for value in peer_values.values())
    if all_peers_true:
        try:
            ipfs.remove_file_from_cluster(cid)
            
            del delete_file_structure[cid]
            
            kv.set_kv(cid, json.dumps(delete_file_structure))
            
            print(f"Successfully deleted file with CID {cid}")
            return True
            
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False
    else:
        print("Cannot delete file: Not all peers have marked it as True")
        return False
    
