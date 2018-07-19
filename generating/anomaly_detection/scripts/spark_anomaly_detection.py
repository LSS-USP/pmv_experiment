from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, udf, get_json_object, array, collect_list
from pyspark.sql.types import *
import json
import os


spark = SparkSession.builder.getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

experiment_to_run = os.getenv("EXPERIMENT_SCENARIO")

if (experiment_to_run == "VALIDATION"):
    model_path = "hdfs://hadoop:9000/hex_model_extended.csv"
elif (experiment_to_run == "CITY_SCALE"):
    model_path = "hdfs://hadoop:9000/traffic_model.csv"
else:
    raise Exception("""
        To use this script, you should override the
        EXPERIMENT_SCENARIO environment variable with
        values "VALIDATION" or "CITY_SCALE"; i.e:
        $ export EXPERIMENT_SCENARIO=VALIDATION
    """)


def load_thresholds():
    df = spark.read.format("csv").option("header", "true").load(model_path)
    thresholds = {}
    model = df.rdd.collect()
    for u in model:
        thresholds[int(u["edgeId"])] = [float(u["lower_threshold"]), float(u["upper_threshold"])]
    return thresholds


def build_kafka_stream(topic):
    return spark.readStream.format('kafka')\
            .option('kafka.bootstrap.servers', 'kafka:9092')\
            .option('subscribe', topic)\
            .option('failOnDataLoss', False)\
            .load()\
            .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")


def mount_json_extraction(cols):
    json_objects = []
    for u in cols:
        json_objects.append(get_json_object(stream.value, '$.'+u).alias(u))
    return json_objects


def mountValue(edgeId):
    return json.dumps({"edgeId": edgeId})


if __name__ == '__main__':
    print("Loading model...")
    thresholds = load_thresholds()
    print("Model loading completed...")

    stream = build_kafka_stream('data_stream')

    json_objects = mount_json_extraction(["edge_id", "avg_speed"])

    def checkAnomaly(edge_id, avg_speed):
        bounds = thresholds.get(int(edge_id), None)
        if (bounds == None):
            return False

        if (float(avg_speed) < bounds[0]):
            return True
        else:
            return False

    udfCheckAnomaly = udf(checkAnomaly, BooleanType())
    udfMountValue = udf(mountValue, StringType())

    anomaly_detection = stream\
            .select(json_objects)\
            .withColumn("is_anomaly", udfCheckAnomaly(col("edge_id"), col("avg_speed")))

    (anomaly_detection
            .filter(col("is_anomaly") == True)
            .select(udfMountValue(col("edge_id")).alias("value"))
            .writeStream.format("kafka")
            .option("kafka.bootstrap.servers", "kafka:9092")
            .option("topic", "anomalies")
            .option("checkpointLocation", "hdfs://hadoop:9000/")
            .trigger(processingTime ='0 seconds')
            .outputMode("append")
            .start())

    (anomaly_detection
            .filter(col("is_anomaly") == True)
            .writeStream
            .outputMode("append")
            .format("console").option("truncate", False)
            .trigger(processingTime='1 seconds')
            .start()
            .awaitTermination())
