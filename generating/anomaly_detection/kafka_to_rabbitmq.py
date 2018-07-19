#!/usr/bin/env python
import pika
from kafka import KafkaConsumer
import json
import utm
import requests
from xml.dom import minidom

# rabbitmq config
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='traffic_sign', exchange_type='topic')

# kafka config
consumer = KafkaConsumer('anomalies')

def loadNodes():
    dom = minidom.parse("map.xml")\
            .getElementsByTagName('node')
    mylist = []
    for u in dom:
        mylist.append([
            int(u.getAttribute('id')),
            float(u.getAttribute('x')),
            float(u.getAttribute('y'))
        ])
    return mylist


def load_edges():
    dom = minidom.parse("map.xml")\
            .getElementsByTagName('link')
    results = {}
    for u in dom:
        results[int(u.getAttribute('id'))] = [
            int(u.getAttribute('from')),
            int(u.getAttribute('to'))
        ]

    return results


print("Loading nodes...")
nodes = {}
for u in loadNodes():
    nodes[u[0]] = [u[1], u[2]]
print("Nodes loaded...")

print("Loading edges...")
edges = load_edges()
print("edges loaded...")


def from_xy_to_latlon(x, y):
    url = "https://epsg.io/trans?data={0},{1}&s_srs=32719&t_srs=4326".format(x, y)
    coords = requests.get(url).json()[0]
    return [float(coords["y"]), float(coords["x"])]


def from_latlon_to_xy(lat, lon):
    url = "https://epsg.io/trans?data={0},{1}&s_srs=4326&t_srs=32719".format(lat, lon)
    coords = requests.get(url).json()[0] 
    return [float(coords["x"]), float(coords["y"])]


for msg in consumer:
    print("***Anomaly detected***")
    payload = msg.value
    anomaly = json.loads(payload)
    print("anomaly => ", anomaly)

    edge_id = anomaly.get("edgeId", None)
    if (edge_id == None):
        raise Exception("Invalid edgeId!!!")
    edge_id = int(edge_id)

    [from_id, to_id] = edges[edge_id]
    coordinates = nodes[from_id]
    converted_coords = from_xy_to_latlon(coordinates[0], coordinates[1])
    
    host = "http://localhost:8000/discovery/"
    endpoint = ("resources?capability=traffic_board&lat={0}&lon={1}&radius=1000"
            .format(converted_coords[0], converted_coords[1]))
    resp = requests.get(host + endpoint)
    resources = json.loads(resp.text)["resources"]
    print("resources: ", resources)

    for r in resources:
        board_id = r.get("description")
        if (board_id == None):
            raise Exception("""
            Your board resources are incorrect. In their description
            you must have their ids.
            """)

        message = "%s.%s.%s" % (board_id, from_id, to_id)
        channel.basic_publish(exchange='traffic_sign',
                               routing_key='#',
                               body=message)

        message = "%s.%s.%s" % (board_id, to_id, from_id)
        channel.basic_publish(exchange='traffic_sign',
                               routing_key='#',
                               body=message)

    #print(" [x] Sent %r" % msg)
    # except:
    #     raise Exception("""
    #         Your resource_discovery looks weird.
    #         Usage: `$python3 kafka_to_rabbitmq.py {resource_discovery_url}`
    #         (default resource_discovery_url: http://localhost:8000/discovery/)
    #     """)
