from xml.dom import minidom
import sys
import requests
from scipy import spatial
import random


def publish_on_platform(node):
    node_id, lat, lon = node

    host = "localhost:8000"
    print("[I] Creating traffic board in node {0}".format(node_id))

    board_json = { "data": {
                            "description": node_id,
                            "capabilities": [ "traffic_board" ],
                            "status": "active",
                            "lat": lat,
                            "lon": lon
                         }
               }

    print("Creating board with the following json: %s" % board_json)
    
    response = requests.post('http://' + host + '/catalog/resources',
                             json=board_json)
    if response.status_code == 404:
        print("[E] Traffic board at node {0} was not created".format(node[0]))
    else:
        print("Resource publish'd...")


def grant_capability_exist():
    url = "http://localhost:8000/catalog/capabilities"
    requests.post(url, {"name": "traffic_board", "capability_type": "sensor"})


if __name__ == '__main__':
    if (len(sys.argv) > 2):
        grant_capability_exist()
        _, nodeid, lat, lon = sys.argv
        publish_on_platform([nodeid, lat, lon])

    else:
        raise Exception("Usage: `generate_and_publish_signs.py nodeid lat lon`")
