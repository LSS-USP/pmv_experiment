# Anomaly Detection System

To run the anomaly detection system you should run the correct model for the
desired scenario and then run detection system itself.

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
