#!/usr/bin/env python

from kafka import KafkaProducer
import pika
from xml.dom import minidom
import json
import os

producer = KafkaProducer(bootstrap_servers='localhost:9092')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='data_stream',
                         exchange_type='topic')


result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue

channel.queue_bind(exchange='data_stream',
                    routing_key = '*.current_location.simulated',
                   queue=queue_name)

experiment_to_run = os.getenv("EXPERIMENT_SCENARIO", None)

if (experiment_to_run == "VALIDATION"):
    map_path = "../../validation/inputs/hex_map.xml"
elif (experiment_to_run == "CITY_SCALE"):
    map_path = "../../city_scale/inputs/map.xml"
else:
    raise Exception("""
        To use this script, you should override the
        EXPERIMENT_SCENARIO environment variable with
        values "VALIDATION" or "CITY_SCALE"; i.e:
        $ export EXPERIMENT_SCENARIO=VALIDATION
    """)


def load_edges():
    dom = minidom.parse(map_path).getElementsByTagName('link')
    results = {}
    for u in dom:
        results[int(u.getAttribute('id'))] = float(u.getAttribute('length'))
    return results


print("Loading map...")
db = {}
edges = load_edges()
print("Map loading complete...")

def callback(ch, method, properties, body):
    payload = json.loads(body)
    prev_point = db.get(payload["uuid"])
    if (prev_point != None):
        prev_tick, prev_edge_id = prev_point
        new_tick, edge_id = (payload["tick"], payload["nodeID"])
        if (new_tick > prev_tick):
            edge_length = edges.get(int(edge_id), None)

            velocity_data = {
                "edge_id": edge_id,
                "avg_speed": edge_length / (new_tick - prev_tick)
            }

            producer.send('data_stream', json.dumps(velocity_data).encode())
        else:
            print("Wrong tick arrived! WARNING")
    db[payload["uuid"]] = (payload["tick"], payload["nodeID"])

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)


print("Ready to transfer data from RabbitMQ to Kafka...")
channel.start_consuming()
