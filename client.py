import kv_service as kv
import ipfs_cluster as ipfs
import json
import os

from kv_service import get_kv

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


def download_file(cid: str, file_path: str):
    """
    This function will download file with cid to file_path
    :param cid: The file CID that user wants to download
    :param file_path: The file path where user wants to save the file(include file name suche like test.txt)
    """
    ipfs.download_file_from_ipfs(cid, file_path)


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





