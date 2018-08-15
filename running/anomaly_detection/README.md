# Anomaly Detection System

To run the anomaly detection system you should run the correct model for the
desired scenario and then run detection system itself. We recommend starting
from the last section (Troubleshooting) before attempting to run the
anomaly detection.

## Running the Validation Experiment

To run our validation experiment you should:

1. Have a Python 3.6 environment with the packages listed in
`dependencies/requirements` file. To install the packages, run:

```
$ pip3.6 install -r dependencies/requirements
```

2. Override the environment variable that defines which experiment will run:

```
$ export EXPERIMENT_SCENARIO=VALIDATION
```

3. Have our anomaly detection Docker containers running. Run:

```
$ docker-compose -f validation-docker-compose.yml up -d
```

4. Check the Docker containers status and be sure that they are all running:

```
$ docker-compose -f validation-docker-compose.yml ps
```

It should look like this:

```
 Name           Command          State                                                 Ports                                              
------------------------------------------------------------------------------------------------------------------------------------------
hadoop   /etc/bootstrap.sh -d    Up      19888/tcp, 2122/tcp, 49707/tcp, 0.0.0.0:50010->50010/tcp, 50020/tcp, 0.0.0.0:50070->50070/tcp,   
                                         50075/tcp, 50090/tcp, 0.0.0.0:8020->8020/tcp, 8030/tcp, 8031/tcp, 8032/tcp, 8033/tcp, 8040/tcp,  
                                         8042/tcp, 8088/tcp, 0.0.0.0:9000->9000/tcp                                                       
kafka    supervisord -n          Up      0.0.0.0:2181->2181/tcp, 0.0.0.0:9092->9092/tcp                                                   
master   /scripts/spark_master   Up      0.0.0.0:4040->4040/tcp, 0.0.0.0:6066->6066/tcp, 7001/tcp, 7002/tcp, 7003/tcp, 7004/tcp, 7005/tcp,
                                         7006/tcp, 0.0.0.0:7077->7077/tcp, 0.0.0.0:9999->9999/tcp                                         
worker   /scripts/spark_worker   Up      4040/tcp, 6066/tcp, 7001/tcp, 7002/tcp, 7003/tcp, 7004/tcp, 7005/tcp, 7006/tcp, 7012/tcp,        
                                         7013/tcp, 7014/tcp, 7015/tcp, 7016/tcp, 7077/tcp, 0.0.0.0:8081->8081/tcp, 8881/tcp, 9999/tcp     
```


5. Run our script that converts RabbitMQ data to Kafka:

```
$ python3 scripts/rabbitmq_to_kafka.py
```

6. Run our script that converts Kafka data to RabbitMQ:

```
$ python3 scripts/kafka_to_rabbitmq.py
```

7. Run the anomaly detection:

```
$ docker exec -it master detect_anomalies
```

## Running the City Scale Experiment

To run our city scale experiment you should:

1. Have a Python 3.6 environment with the packages listed in
`dependencies/requirements` file. To install the packages, run:

```
$ pip3.6 install -r dependencies/requirements
```

2. Override the environment variable that defines which experiment will run:

```
$ export EXPERIMENT_SCENARIO=CITY_SCALE
```

3. Have our anomaly detection Docker containers running. Run:

```
$ docker-compose -f city-scale-docker-compose.yml up -d
```

4. Check the Docker containers status and be sure that they are all running:

```
$ docker-compose -f city-scale-docker-compose.yml ps
```

It should look like this:

```
 Name           Command          State                                                 Ports                                              
------------------------------------------------------------------------------------------------------------------------------------------
hadoop   /etc/bootstrap.sh -d    Up      19888/tcp, 2122/tcp, 49707/tcp, 0.0.0.0:50010->50010/tcp, 50020/tcp, 0.0.0.0:50070->50070/tcp,   
                                         50075/tcp, 50090/tcp, 0.0.0.0:8020->8020/tcp, 8030/tcp, 8031/tcp, 8032/tcp, 8033/tcp, 8040/tcp,  
                                         8042/tcp, 8088/tcp, 0.0.0.0:9000->9000/tcp                                                       
kafka    supervisord -n          Up      0.0.0.0:2181->2181/tcp, 0.0.0.0:9092->9092/tcp                                                   
master   /scripts/spark_master   Up      0.0.0.0:4040->4040/tcp, 0.0.0.0:6066->6066/tcp, 7001/tcp, 7002/tcp, 7003/tcp, 7004/tcp, 7005/tcp,
                                         7006/tcp, 0.0.0.0:7077->7077/tcp, 0.0.0.0:9999->9999/tcp                                         
worker   /scripts/spark_worker   Up      4040/tcp, 6066/tcp, 7001/tcp, 7002/tcp, 7003/tcp, 7004/tcp, 7005/tcp, 7006/tcp, 7012/tcp,        
                                         7013/tcp, 7014/tcp, 7015/tcp, 7016/tcp, 7077/tcp, 0.0.0.0:8081->8081/tcp, 8881/tcp, 9999/tcp     
```


5. Run our script that converts RabbitMQ data to Kafka:

```
$ python3 scripts/rabbitmq_to_kafka.py
```

6. Run our script that converts Kafka data to RabbitMQ:

```
$ python3 scripts/kafka_to_rabbitmq.py
```

7. Run the anomaly detection:

```
$ docker exec -it master detect_anomalies
```

## Troubleshooting

In this section we present a few common problems and how to solve them.

### Hadoop in Safe Mode

From time to time, after starting the hadoop container, theres a chance of
occurring the following error:

```
org.apache.hadoop.hdfs.server.namenode.SafeModeException: Cannot create file/metadata. Name node is in safe mode.                         
The reported blocks 231 has reached the threshold 0.9990 of total blocks 231. The number of live datanodes 1 has reached the minimum numbe
r 0. In safe mode extension. Safe mode will be turned off automatically in 8 seconds.                                                     
        at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.checkNameNodeSafeMode(FSNamesystem.java:1327)                              
        at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.startFileInt(FSNamesystem.java:2424)                                       
        at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.startFile(FSNamesystem.java:2312)                                          
        at org.apache.hadoop.hdfs.server.namenode.NameNodeRpcServer.create(NameNodeRpcServer.java:622)                                            at org.apache.hadoop.hdfs.protocolPB.ClientNamenodeProtocolServerSideTranslatorPB.create(ClientNamenodeProtocolServerSideTranslatorPB.java:397)
```

It means that you Hadoop just started and its name nodes are still in safe mode.
To fix it you can just wait or:

1. Enter in the hadoop container:

```
$ docker exec -it hadoop /bin/bash
```

2. Enter in the hadoop folder:

```
$ cd $HADOOP_PREFIX
```

3. Run the following command:

```
$ ./bin/hdfs dfsadmin -safemode leave
```
