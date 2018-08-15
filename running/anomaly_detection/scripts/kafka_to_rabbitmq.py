#!/usr/bin/env python
import pika
from kafka import KafkaConsumer
import json
import utm
import requests
import os
from xml.dom import minidom
import datetime

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='traffic_sign', exchange_type='topic')

consumer = KafkaConsumer('anomalies')

experiment_to_run = os.getenv("EXPERIMENT_SCENARIO", None)

if (experiment_to_run == "VALIDATION"):
    map_path = "../../validation/inputs/hex_map.xml"
elif (experiment_to_run == "CITY_SCALE"):
    map_path = "./map_complete.xml"
else:
    raise Exception("""
        To use this script, you should override the
        EXPERIMENT_SCENARIO environment variable with
        values "VALIDATION" or "CITY_SCALE"; i.e:
        $ export EXPERIMENT_SCENARIO=VALIDATION
    """)


def load_nodes():
    dom = minidom.parse(map_path)\
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
    dom = minidom.parse(map_path)\
            .getElementsByTagName('link')
    results = {}
    for u in dom:
        results[int(u.getAttribute('id'))] = [
            int(u.getAttribute('from')),
            int(u.getAttribute('to'))
        ]

    return results


print("Loading map nodes...")
nodes = {}
for u in load_nodes():
    nodes[u[0]] = [u[1], u[2]]
print("Map nodes loaded...")

print("Loading map edges...")
edges = load_edges()
print("Map edges loaded...")


def from_xy_to_latlon(x, y):
    url = "https://epsg.io/trans?data={0},{1}&s_srs=32719&t_srs=4326".format(x, y)
    coords = requests.get(url).json()[0]
    return [float(coords["y"]), float(coords["x"])]


def from_latlon_to_xy(lat, lon):
    url = "https://epsg.io/trans?data={0},{1}&s_srs=4326&t_srs=32719".format(lat, lon)
    coords = requests.get(url).json()[0] 
    return [float(coords["x"]), float(coords["y"])]

print("Ready to transfer data from Kafka to RabbitMQ...")
import csv

with open('round.csv', 'a', newline='') as fil:
    mywriter = csv.writer(fil)

    for msg in consumer:
        print("Anomaly detected...")
        payload = msg.value

        anomaly = json.loads(payload)

        edge_id = anomaly.get("edgeId", None)
        edge_id = int(edge_id)
        measure_id = anomaly.get("measure_id", None)
        timestamp = anomaly.get("timestamp", None)

        [from_id, to_id] = edges[edge_id]
        coordinates = nodes[from_id]
        
        host = "http://localhost:8000/discovery/"
        endpoint = ("resources?capability=traffic_board&lat={0}&lon={1}&radius=1000"
                .format(coordinates[0], coordinates[1]))
        resp = requests.get(host + endpoint)
        resources = json.loads(resp.text)["resources"]

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

            new_timestamp = datetime.datetime.utcnow().isoformat()
            print("writing...")
            fil.write("{0};{1};{2}\n".format(measure_id, timestamp, new_timestamp))
